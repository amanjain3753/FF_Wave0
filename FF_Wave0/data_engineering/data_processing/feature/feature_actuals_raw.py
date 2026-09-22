from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

from mwd30anaplan.data_engineering.data_processing.constants import ACTUALS_RAW

spark = SparkSession.builder.getOrCreate()


def get_actuals_raw(
    df_facts_source: DataFrame,
    df_ep_source: DataFrame,
    df_ac_id_filters: DataFrame,
    df_entity_id_filter: DataFrame,
    year_period_list: list,
) -> tuple[DataFrame, DataFrame]:
    """
    Filter the source financial fact views down to the accounts, entities and
    periods required by Anaplan and return the two RAW-zone DataFrames.

    These are the exact source facts that ACTUALS_PROCESS later reads back from
    the RAW zone as ``facts_financial_consolidated_customer`` and
    ``ep_account_entity``. This step only filters and materialises the source
    views — the heavy joins/aggregation still happen in ACTUALS_PROCESS.

    Args:
        df_facts_source (DataFrame): Customer destination RLS account/entity view.
        df_ep_source (DataFrame): EP RLS account/entity view.
        df_ac_id_filters (DataFrame): Account ID filter file with Type column
            (Actuals/EP).
        df_entity_id_filter (DataFrame): Entity ID filter file controlling BU
            inclusion.
        year_period_list (list): Date_ID / Source_Date_ID integers to keep
            (e.g. [202501, 202502]). The customer view is filtered on Date_ID
            and the EP view on Source_Date_ID.

    Returns:
        tuple[DataFrame, DataFrame]: (customer RAW DataFrame, EP RAW DataFrame).
    """
    # ── yearperiod string for the IN clause ───────────────────────────────────
    yearperiod = ",".join(map(str, year_period_list))

    # ── Filter lists from the mapping files ───────────────────────────────────
    entity_ids = [row["entity_id"] for row in df_entity_id_filter.collect()]
    ac_filters_actuals = [
        row["account_id"]
        for row in df_ac_id_filters.filter(col("type") == "Actuals").collect()
    ]
    ac_filters_ep = [
        row["account_id"]
        for row in df_ac_id_filters.filter(col("type") == "EP").collect()
    ]
    

    account_list = ",".join(f"'{a}'" for a in ac_filters_actuals)
    account_list_ep = ",".join(f"'{a}'" for a in ac_filters_ep)
    entity_list = ",".join(f"'{e}'" for e in entity_ids)

    # ── Register source views for SQL filtering ───────────────────────────────
    df_facts_source.createOrReplaceTempView("raw_customer_source")
    df_ep_source.createOrReplaceTempView("raw_ep_source")

    # ── Customer RAW ──────────────────────────────────────────────────────────
    df_customer_raw = spark.sql(
        ACTUALS_RAW.customer_query.format(
            account_list=account_list,
            entity_list=entity_list,
            yearperiod=yearperiod,
        )
    )

    # ── EP RAW ────────────────────────────────────────────────────────────────
    df_ep_raw = spark.sql(
        ACTUALS_RAW.ep_query.format(
            account_list_ep=account_list_ep,
            entity_list=entity_list,
            yearperiod=yearperiod,
        )
    )

    return df_customer_raw, df_ep_raw
