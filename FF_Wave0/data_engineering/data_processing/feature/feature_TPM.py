from pyspark.sql import DataFrame, SparkSession

from mwd30anaplan.data_engineering.data_processing.constants import TPM_PROCESSING

spark = SparkSession.builder.getOrCreate()


def get_TPM(
    df_fact_account_plan: DataFrame,
    df_dim_cust_sales: DataFrame,
    df_dim_material: DataFrame,
    df_dim_calendar_tpm: DataFrame,
    df_fact_internal_product_week: DataFrame,
    df_dim_manual_kpis: DataFrame,
) -> DataFrame:
    """
    Build unified Trade Promo Management (TPM) dataset from silver tables
    and manual CCA/MX files.

    Sources:
        - NA  (LIVE snapshot, Total_Trade available)
        - CA (salesorg 121, calculated Total Trade via CTEs)
        - MX (manual file)
        - CCA (manual file + hardcoded mapping)

    Args:
        df_fact_account_plan (DataFrame): TPM fact table with weekly account plan data.
        df_dim_cust_sales (DataFrame): Customer sales dimension with plan account and demand group.
        df_dim_material (DataFrame): Material dimension with Rep_Item_ID.
        df_dim_calendar_tpm (DataFrame): Mars calendar table (global_utilities_mars_calendar_all).
        df_fact_internal_product_week (DataFrame): CA promo KPIs aggregated by week.
        df_dim_manual_kpis (DataFrame): CA manual KPIs aggregated by week.

    Returns:
        DataFrame: Final TPM DataFrame registered as temp view 'tpm'.
    """
    # ── Register temp views ───────────────────────────────────────────────────
    df_fact_account_plan.createOrReplaceTempView("fact_account_plan")
    df_dim_cust_sales.createOrReplaceTempView("dim_cust_sales")
    df_dim_material.createOrReplaceTempView("dim_material")
    df_dim_calendar_tpm.createOrReplaceTempView("dim_calendar_tpm")
    df_fact_internal_product_week.createOrReplaceTempView("fact_internal_product_week")
    df_dim_manual_kpis.createOrReplaceTempView("dim_manual_kpis")

    # ── CCA mapping inline ────────────────────────────────────────────────────
    spark.createDataFrame(
        [
            ("Costa Rica", "40130458", "282"),
            ("Cuba", "40130459", "145"),
            ("Dominicana", "40130460", "145"),
            ("El Salvador", "40130461", "145"),
            ("GBS", "40130576", "145"),
            ("Guatemala", "40130462", "499"),
            ("Honduras", "40130463", "145"),
            ("IKA", "40130465", "145"),
            ("MTC Puerto Rico", "40130299", "144"),
            ("Nicaragua", "40130464", "145"),
            ("Panama", "40130467", "280"),
            ("ROC", "40130466", "145"),
            ("TTC Puerto Rico", "40130300", "144"),
        ],
        ["country_name", "demand_group_code", "mapped_sales_org"],
    ).createOrReplaceTempView("cca_demand_group_map")

    # ── 1) NA Silver ─────────────────────────────────────────────────────────
    df_na = spark.sql(TPM_PROCESSING.na_silver_query)

    # ── 2) CA ─────────────────────────────────────────────────────────────────
    df_ca = spark.sql(TPM_PROCESSING.ca_query)

    # ── Union all ─────────────────────────────────────────────────────────────
    df_combined = df_na.unionByName(df_ca)
    df_combined.createOrReplaceTempView("tpm_combined")

    # ── Final select with unique_key ─────────────────────────────────────────
    df_tpm = spark.sql(TPM_PROCESSING.final_select)

    return df_tpm
