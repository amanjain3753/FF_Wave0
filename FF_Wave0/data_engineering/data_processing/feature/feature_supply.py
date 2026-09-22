from datetime import date, datetime

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from mwd30anaplan.data_engineering.data_processing.constants import (
    PROCESSING_CONST as const,
)
from mwd30anaplan.data_engineering.data_processing.constants import (
    SUPPLY_PROCESSING,
)

spark = SparkSession.builder.getOrCreate()


def get_supply_all(
    df_despatched: DataFrame,
    df_production_unit: DataFrame,
    df_production_tonnes: DataFrame,
    df_latam: DataFrame,
    df_mars_calendar: DataFrame,
    df_uom: DataFrame,
    df_salesorg: DataFrame,
    df_material_master: DataFrame,
    process_date: str,
) -> DataFrame:
    """
    Build unified Supply dataset from Despatched and Production sources (NA + LATAM).
    Registers all inputs as temp views, builds shared lookup views,
    executes per-source queries, and unions into final output.

    Args:
        df_despatched (DataFrame): NA despatched supply data from Kinaxis.
        df_production_unit (DataFrame): NA production volumes in units from Kinaxis.
        df_production_tonnes (DataFrame): NA production volumes in tonnes from Kinaxis.
        df_latam (DataFrame): LATAM supply plan data from Kinaxis.
        df_mars_calendar (DataFrame): Mars calendar mapping file.
        df_uom (DataFrame): Unit of measure masterdata.
        df_salesorg (DataFrame): Sales org to site mapping file.
        df_material_master (DataFrame): Product masterdata for material enrichment.
        process_date (str): W2 Tuesday anchor date resolved by trigger_date_check.
            Every source is locked to its newest snapshot on or before this date
            instead of the newest snapshot in the table.

    Returns:
        DataFrame: Final unified supply DataFrame registered as temp view 'supply'.
    """
    if isinstance(process_date, (datetime, date)):
        process_date = process_date.strftime("%Y-%m-%d")
    else:
        process_date = str(process_date).strip()[:10]

    # The NA Kinaxis tables store as_of_dt as YYYYMMDD, LATAM stores YYYY-MM-DD,
    # so the anchor has to be handed to each query in the format that source uses.
    process_date_compact = process_date.replace("-", "")

    # ── Register source temp views ───────────────────────────────────────────
    df_despatched.createOrReplaceTempView("Despatched")
    df_production_unit.createOrReplaceTempView("production_Volumes_unit")
    df_production_tonnes.createOrReplaceTempView("production_Volumes_tonnes")
    df_latam.createOrReplaceTempView("df_latam")
    df_mars_calendar.createOrReplaceTempView("mars_calendar")
    df_uom.createOrReplaceTempView("uom")
    df_salesorg.createOrReplaceTempView("salesorg")
    df_material_master.createOrReplaceTempView("material_master")

    # ── Shared lookup views ──────────────────────────────────────────────────
    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_ea_to_cs AS
    SELECT
      Material_ID,
      CAST(Numerator_to_base_unit_Conversion AS DOUBLE) AS num,
      CAST(denominator_to_base_unit_conversion AS DOUBLE) AS den
    FROM uom
    WHERE Base_Unit = 'EA' AND To_Base_Unit = 'CS'
    """
    )

    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_ea_to_kg AS
    SELECT
      Material_ID,
      CASE
        WHEN Base_Weight_Unit = 'KG' THEN CAST(Net_Weight AS DOUBLE) * 1.0
        WHEN Base_Weight_Unit = 'G'  THEN CAST(Net_Weight AS DOUBLE) * 0.001
        WHEN Base_Weight_Unit = 'MG' THEN CAST(Net_Weight AS DOUBLE) * 0.000001
        WHEN Base_Weight_Unit = 'OZ' THEN CAST(Net_Weight AS DOUBLE) * 0.02835
        WHEN Base_Weight_Unit = 'LB' THEN CAST(Net_Weight AS DOUBLE) * 0.4536
        WHEN Base_Weight_Unit = 'TO' THEN CAST(Net_Weight AS DOUBLE) * 1000
      END AS kg_per_ea
    FROM uom
    WHERE Base_Unit = 'EA' AND To_Base_Unit = 'EA'
      AND Base_Weight_Unit IS NOT NULL AND Base_Weight_Unit != 'null'
    """
    )

    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_base_uom AS
    SELECT Material_ID, Base_Unit
    FROM (
      SELECT Material_ID, Base_Unit,
        ROW_NUMBER() OVER (PARTITION BY Material_ID ORDER BY Base_Unit) AS rn
      FROM (SELECT DISTINCT Material_ID, Base_Unit FROM uom)
    ) WHERE rn = 1
    """
    )

    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_material_tdu AS
    SELECT Material_ID, TDU
    FROM (
      SELECT Material_ID, TDU,
        ROW_NUMBER() OVER (PARTITION BY Material_ID ORDER BY TDU) AS rn
      FROM (SELECT DISTINCT Material_ID, TDU FROM uom)
    ) WHERE rn = 1
    """
    )

    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_material_master AS
    SELECT DISTINCT `Material_SKU` AS Material_SKU, ZREP
    FROM material_master
    """
    )

    # ── Per-source queries ────────────────────────────────────────────────────
    df_despatched_na = spark.sql(
        SUPPLY_PROCESSING.despatched_na_query.format(process_date=process_date_compact)
    )
    df_despatched_latam = spark.sql(
        SUPPLY_PROCESSING.despatched_latam_query.format(process_date=process_date)
    )
    df_production_na = spark.sql(
        SUPPLY_PROCESSING.production_na_query.format(process_date=process_date_compact)
    )
    df_production_latam = spark.sql(
        SUPPLY_PROCESSING.production_latam_query.format(process_date=process_date)
    )

    # ── Union all sources ────────────────────────────────────────────────────
    df_supply_all = (
        df_despatched_na.unionByName(df_despatched_latam)
        .unionByName(df_production_na)
        .unionByName(df_production_latam)
    )

    # ── Unique key ────────────────────────────────────────────────────────────
    df_supply_all = df_supply_all.withColumn(
        const.UNIQUE_KEY,
        F.concat_ws(
            "_",
            F.coalesce(F.col(const.MATERIAL_NUMBER), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(
            F.col(const.SALES_ORG).cast("string"), F.lit(const.DEFAULT_ZERO_3)
            ),
            F.coalesce(F.col(const.PART_SITE), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(F.col(const.DEMAND_TYPE), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(F.col(const.DESTINATION_SITE), F.lit(const.DEFAULT_ZERO_3)),
        ),
    )

    # ── Final column order ───────────────────────────────────────────────────
    df_supply_all = df_supply_all.select(
        F.col(const.UNIQUE_KEY),
        F.col(const.DEMAND_TYPE),
        F.col(const.PART_SITE),
        F.col(const.DESTINATION_SITE),
        F.col(const.MATERIAL_NUMBER),
        F.col(const.MATERIAL_DESCRIPTION),
        F.col(const.ZREP),
        F.col(const.FISCAL_YEAR_PERIOD),
        F.col(const.VOLUME_CASES),
        F.col(const.VOLUME_TONNES),
        F.col(const.SALES_ORG).cast("string").alias(const.SALES_ORG),
    )

    return df_supply_all

 
