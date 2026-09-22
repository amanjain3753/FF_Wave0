import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, expr
from pyspark.sql.functions import max as spark_max

from mwd30anaplan.data_engineering.data_processing.constants import (
    ACTUALS_PROCESSING,
)
from mwd30anaplan.data_engineering.data_processing.constants import (
    PROCESSING_CONST as const,
)

spark = SparkSession.builder.getOrCreate()


def get_actuals(
    df_facts_financial_consolidated_customer: DataFrame,
    df_ep_account_entity: DataFrame,
    df_dimension_entity: DataFrame,
    df_dimensions_account: DataFrame,
    df_dimensions_item_taxonomy: DataFrame,
    df_dimensions_currency: DataFrame,
    df_dimensions_customer: DataFrame,
    df_product: DataFrame,
    df_customer_master: DataFrame,
    df_ac_id_filters: DataFrame,
    df_entity_id_filter: DataFrame,
    year_period_list: list,
) -> DataFrame:
    """
    Build final Actuals dataset from Customer and EP actuals sources.

    Args:
        df_facts_financial_consolidated_customer (DataFrame): Customer financial fact table.
        df_ep_account_entity (DataFrame): EP financial fact table.
        df_dimension_entity (DataFrame): Entity dimension.
        df_dimensions_account (DataFrame): Account dimension.
        df_dimensions_item_taxonomy (DataFrame): Item taxonomy dimension.
        df_dimensions_currency (DataFrame): Currency dimension with FX rates.
        df_dimensions_customer (DataFrame): Customer dimension with KUNNR.
        df_product (DataFrame): Product masterdata with Material/SKU and Material Desc.
        df_customer_master (DataFrame): Customer masterdata with Customer and Customer Desc.
        df_ac_id_filters (DataFrame): Account ID filter file with Type column (Actuals/EP).
        df_entity_id_filter (DataFrame): Entity ID filter file controlling BU inclusion.
        year_period_list (list): List of Date_ID integers to process (e.g. [202501, 202502]).

    Returns:
        DataFrame: Final aggregated actuals with Code, Fiscal_Year_Period,
            dimensions, and summed Value.
    """

    # ── Fact tables ───────────────────────────────────────────────────────────
    df_facts_financial_consolidated_customer.createOrReplaceTempView(
        "facts_financial_consolidated_customer"
    )
    df_ep_account_entity.createOrReplaceTempView("ep_account_entity")

    # ── Dimension tables ──────────────────────────────────────────────────────
    df_dimension_entity.createOrReplaceTempView("dimensions_Entity")
    df_dimensions_account.createOrReplaceTempView("dimensions_Account")
    df_dimensions_item_taxonomy.createOrReplaceTempView("dimensions_Item_Taxonomy")
    df_dimensions_currency.createOrReplaceTempView("dimensions_currency")
    df_dimensions_customer.createOrReplaceTempView("dimensions_customer")

    # ── Filter views ──────────────────────────────────────────────────────────
    df_entity_id_filter.select(const.ENTITY_ID).distinct().createOrReplaceTempView(
        "entity_filters"
    )

    df_ac_id_filters.filter(col("type") == "Actuals").createOrReplaceTempView(
        "ac_filters"
    )

    df_ac_id_filters.filter(col("type") == "EP").createOrReplaceTempView(
        "rl_filters_ep"
    )

    # ── Product lookup (deduped) ──────────────────────────────────────────────
    (
        df_product.withColumn(
            "Material_SKU", expr("TRY_CAST(`Material_SKU` AS BIGINT)")
        )
        .filter(col("`Material_SKU`").isNotNull())
        .groupBy("`Material_SKU`")
        .agg(spark_max("`Material_Desc`").alias("Material_Desc"))
        .createOrReplaceTempView("product_lookup")
    )

    # ── Customer master (deduped) ─────────────────────────────────────────────
    (
        df_customer_master.groupBy(const.CUSTOMER)
        .agg(spark_max("`Customer Desc`").alias("Customer_Description"))
        .createOrReplaceTempView("customer_dedup")
    )

    # ── yearperiod string for IN clause ──────────────────────────────────────
    yearperiod = ",".join(map(str, year_period_list))

    # ── Customer base ─────────────────────────────────────────────────────────
    customer_base = spark.sql(
        ACTUALS_PROCESSING.customer_base_query.format(yearperiod=yearperiod)
    )

    # ── EP base ───────────────────────────────────────────────────────────────
    ep_base = spark.sql(ACTUALS_PROCESSING.ep_base_query.format(yearperiod=yearperiod))

    # ── Union + enrichment ────────────────────────────────────────────────────
    customer_base.unionByName(ep_base).createOrReplaceTempView("combined_base")

    final_combined = spark.sql(ACTUALS_PROCESSING.final_combined_query)

    # ── Final aggregation ─────────────────────────────────────────────────────
    key_cols = [const.CODE, const.FISCAL_YEAR_PERIOD_CAPS]
    desc_cols = [c for c in final_combined.columns if c not in key_cols + [const.VALUE]]
    final_aggregated = final_combined.groupBy(key_cols).agg(
        *[F.max(c).alias(c) for c in desc_cols], F.sum(const.VALUE).alias(const.VALUE)
    )
    return final_aggregated
