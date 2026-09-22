from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from datetime import date, datetime
from mwd30anaplan.data_engineering.data_processing.constants import (
    DEMAND_PROCESSING,
)
from mwd30anaplan.data_engineering.data_processing.constants import (
    PROCESSING_CONST as const,
)

spark = SparkSession.builder.getOrCreate()


def get_demand(
    df_comb_na: DataFrame,
    df_latm_consensus: DataFrame,
    df_latm_preconsensus: DataFrame,
    df_cca: DataFrame,
    df_mars_calendar: DataFrame,
    df_uom: DataFrame,
    df_salesorg: DataFrame,
    df_customer: DataFrame,
    df_product: DataFrame,
    df_forecast_mapping: DataFrame,
    df_bb_mapping: DataFrame,
    df_na_consensus: DataFrame,
    process_date: str,
) -> DataFrame:
    """
    Build unified Demand dataset from NA (combined consensus+preconsensus),
    LATAM Consensus, LATAM Preconsensus, and CCA manual flat file sources.

    Args:
        df_comb_na (DataFrame): NA combined demand forecast (consensus + preconsensus).
        df_latm_consensus (DataFrame): LATAM consensus forecast.
        df_latm_preconsensus (DataFrame): LATAM Kinaxis MX preconsensus forecast detail.
        df_cca (DataFrame): CCA manual demand flat file.
        df_mars_calendar (DataFrame): Mars calendar mapping file.
        df_uom (DataFrame): UOM masterdata for unit conversions.
        df_salesorg (DataFrame): Sales org to site mapping file.
        df_customer (DataFrame): Customer masterdata.
        df_product (DataFrame): Product masterdata.
        df_forecast_mapping (DataFrame): Forecast type ID mapping file.
        df_bb_mapping (DataFrame): Building Block ID mapping file.

    Returns:
        DataFrame: Final unified demand dataset with unique_key, ordered to
            target column schema.
    """
    if isinstance(process_date, (datetime, date)):
        process_date = process_date.strftime("%Y-%m-%d")
    else:
        process_date = str(process_date).strip()[:10]

        process_date = str(process_date).strip()[:10]

    df_mars_calendar.createOrReplaceTempView("marscal")
    # ── Register source temp views ───────────────────────────────────────────
    df_comb_na.createOrReplaceTempView("comb_na")
    df_latm_consensus.createOrReplaceTempView("latm_consensus")
    df_latm_preconsensus.createOrReplaceTempView("latm_preconsensus")
    df_cca.createOrReplaceTempView("cca")
    df_uom.createOrReplaceTempView("uom")
    df_salesorg.createOrReplaceTempView("salesorg")
    df_customer.createOrReplaceTempView("customer")
    df_product.createOrReplaceTempView("product")
    df_forecast_mapping.createOrReplaceTempView("forecast_mapping")
    df_bb_mapping.createOrReplaceTempView("BB_mapping")
    df_na_consensus.createOrReplaceTempView("na_consensus")

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
    CREATE OR REPLACE TEMP VIEW v_product AS
    SELECT `Material_SKU`, `Material_Desc`
    FROM (
      SELECT `Material_SKU`, `Material_Desc`,
        ROW_NUMBER() OVER (PARTITION BY `Material_SKU` ORDER BY `Material_SKU`) AS rn
      FROM product
    ) WHERE rn = 1
    """
    )

    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_customer_by_dg AS
    SELECT `Demand Group`, `Demand Group Desc`, `Sales Org`,
      `Distribution Channel`, Division
    FROM (
      SELECT `Demand Group`, `Demand Group Desc`, `Sales Org`,
        `Distribution Channel`, Division,
        ROW_NUMBER() OVER (PARTITION BY `Demand Group`, `Sales Org` ORDER BY `Demand Group`) AS rn
      FROM customer
    ) WHERE rn = 1
    """
    )

    spark.sql(
        """
    CREATE OR REPLACE TEMP VIEW v_customer_by_id AS
    SELECT Customer, `Customer Desc`, `Demand Group`, `Demand Group Desc`,
      `Sales Org`, `Distribution Channel`, Division
    FROM (
      SELECT Customer, `Customer Desc`, `Demand Group`, `Demand Group Desc`,
        `Sales Org`, `Distribution Channel`, Division,
        ROW_NUMBER() OVER (
          PARTITION BY Customer, `Sales Org`
          ORDER BY CASE WHEN `Demand Group` IS NULL OR `Demand Group` = 'null' THEN 1 ELSE 0 END,
                   `Demand Group`
        ) AS rn
      FROM customer
    ) WHERE rn = 1
    """
    )

    # ── NA ────────────────────────────────────────────────────────────────────
    df_na = spark.sql(DEMAND_PROCESSING.na_query.format(process_date=process_date))

    # ── LATAM Consensus ──────────────────────────────────────────────────────
    df_latm_con = spark.sql(
        DEMAND_PROCESSING.latm_con_query.format(process_date=process_date)
    )

    # ── LATAM Preconsensus ───────────────────────────────────────────────────

    df_latm_pre = spark.sql(
        DEMAND_PROCESSING.latm_pre_query.format(process_date=process_date)
    )

    # ── CCA Demand ────────────────────────────────────────────────────────────
    df_cca_demand = spark.sql(DEMAND_PROCESSING.cca_demand_query)

    # CCA dedup: group by to avoid duplicates from flat-file granularity
    df_cca_demand_agg = df_cca_demand.groupBy(
        const.MATERIAL_NUMBER,
        const.FISCAL_YEAR_PERIOD,
        const.DEMAND_GROUP,
        const.BUILDING_BLOCK_ID,
    ).agg(
        F.max(const.SITE).alias(const.SITE),
        F.max(const.MATERIAL_DESCRIPTION).alias(const.MATERIAL_DESCRIPTION),
        F.max(const.CUSTOMER_ID).alias(const.CUSTOMER_ID),
        F.max(const.CUSTOMER_DESCRIPTION).alias(const.CUSTOMER_DESCRIPTION),
        F.max(const.DEMAND_GROUP_DESCRIPTION).alias(const.DEMAND_GROUP_DESCRIPTION),
        F.max(const.FORECAST_TYPE_ID).alias(const.FORECAST_TYPE_ID),
        F.max(const.FORECAST_TYPE).alias(const.FORECAST_TYPE),
        F.max(const.BUILDING_BLOCK).alias(const.BUILDING_BLOCK),
        F.sum(const.VOLUME_CASES).alias(const.VOLUME_CASES),
        F.sum(const.VOLUME_TONNES).alias(const.VOLUME_TONNES),
        F.max(const.GSV).alias(const.GSV),
        F.max(const.SALES_ORG).alias(const.SALES_ORG),
        F.max(const.DISTRIBUTION_CHANNEL).alias(const.DISTRIBUTION_CHANNEL),
        F.max(const.DIVISION).alias(const.DIVISION),
    )

    # ── Union all sources ────────────────────────────────────────────────────
    df_demand = (
        df_na.unionByName(df_latm_con)
        .unionByName(df_latm_pre)
        .unionByName(df_cca_demand_agg)
    )

    # ── Flag unmapped IDs with 99 ────────────────────────────────────────────
    df_demand = df_demand.withColumn(
        const.FORECAST_TYPE_ID, F.coalesce(F.col(const.FORECAST_TYPE_ID), F.lit(99))
    ).withColumn(
        const.BUILDING_BLOCK_ID, F.coalesce(F.col(const.BUILDING_BLOCK_ID), F.lit(99))
    )

    # ── Unique key ────────────────────────────────────────────────────────────
    df_demand = df_demand.withColumn(
        const.UNIQUE_KEY,
        F.concat_ws(
            "_",
            F.coalesce(F.col(const.MATERIAL_NUMBER), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(F.col(const.SITE), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(F.col(const.CUSTOMER_ID), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(F.col(const.DEMAND_GROUP), F.lit(const.DEFAULT_ZERO_3)),
            F.coalesce(
                F.col(const.FORECAST_TYPE_ID).cast("string"),
                F.lit(const.DEFAULT_ZERO_3),
            ),
            F.coalesce(
                F.col(const.BUILDING_BLOCK_ID).cast("string"),
                F.lit(const.DEFAULT_ZERO_3),
            ),
            F.coalesce(
                F.col(const.SALES_ORG).cast("string"), F.lit(const.DEFAULT_ZERO_3)
            ),
            F.coalesce(
                F.col(const.DIVISION).cast("string"), F.lit(const.DEFAULT_ZERO_3)
            ),
        ),
    )

    # ── Final column order ───────────────────────────────────────────────────
    df_demand = df_demand.select(
        F.col(const.UNIQUE_KEY),
        F.col(const.MATERIAL_NUMBER),
        F.col(const.MATERIAL_DESCRIPTION),
        F.col(const.SITE),
        F.col(const.FISCAL_YEAR_PERIOD),
        F.col(const.CUSTOMER_ID),
        F.col(const.CUSTOMER_DESCRIPTION),
        F.col(const.DEMAND_GROUP),
        F.col(const.DEMAND_GROUP_DESCRIPTION),
        F.col(const.FORECAST_TYPE_ID),
        F.col(const.FORECAST_TYPE),
        F.col(const.BUILDING_BLOCK_ID),
        F.col(const.BUILDING_BLOCK),
        F.col(const.VOLUME_CASES),
        F.col(const.VOLUME_TONNES),
        F.col(const.SALES_ORG),
        F.col(const.GSV),
        F.col(const.DISTRIBUTION_CHANNEL),
        F.col(const.DIVISION),
    )

    return df_demand
