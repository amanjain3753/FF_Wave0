from pyspark.sql import DataFrame, SparkSession

from mwd30anaplan.data_engineering.data_processing.constants import PRICE_PROCESSING

spark = SparkSession.builder.getOrCreate()


def get_customer_price_list(
    df_a501: DataFrame,
    df_a812: DataFrame,
    df_a872: DataFrame,
    df_a865: DataFrame,
    df_a883: DataFrame,
    df_a882: DataFrame,
    df_a513: DataFrame,
    df_a599: DataFrame,
    df_konp: DataFrame,
    df_product_masterdata: DataFrame,
    df_customer_masterdata: DataFrame,
    df_edf_latam_csl_pricing_info: DataFrame,
) -> DataFrame:
    """
    Customer Price List — joins 9 SAP condition tables
    with product_master and customer_master temp views.

    Args:
        df_a501               : Condition table A501
        df_a812               : Condition table A812
        df_a872               : Condition table A872
        df_a865               : Condition table A865
        df_a883               : Condition table A883
        df_a882               : Condition table A882
        df_a513               : Condition table A513
        df_a599               : Condition table A599
        df_konp               : Condition header table KONP
        df_product_masterdata : Product masterdata (from PRODUCT_MASTERDATA process)
        df_customer_masterdata: Customer masterdata (from CUSTOMER_MASTERDATA process)
        df_edf_latam_csl_pricing_info: LATAM CSL pricing, used by the ZM00 branch

    Returns:
        DataFrame: Final Customer Price List
    """

    # ── Register temp views ───────────────────────────────────────────────────
    df_a501.createOrReplaceTempView("A501")
    df_a812.createOrReplaceTempView("A812")
    df_a872.createOrReplaceTempView("A872")
    df_a865.createOrReplaceTempView("A865")
    df_a883.createOrReplaceTempView("A883")
    df_a882.createOrReplaceTempView("A882")
    df_a513.createOrReplaceTempView("A513")
    df_a599.createOrReplaceTempView("A599")
    df_konp.createOrReplaceTempView("KONP")
    df_product_masterdata.createOrReplaceTempView("product_master")
    df_customer_masterdata.createOrReplaceTempView("customer_master")
    df_edf_latam_csl_pricing_info.createOrReplaceTempView("edf_latam_csl_pricing_info")

    df_price = spark.sql(PRICE_PROCESSING.CUSTOMER_PRICE.CUSTOMER_PRICE_QUERY)

    return df_price


def get_standard_cost(
    df_zbw_co_pc_pcp_20: DataFrame,
    df_costcomp_text: DataFrame,
    df_product_masterdata: DataFrame,
) -> DataFrame:
    df_zbw_co_pc_pcp_20.createOrReplaceTempView("ZBW_CO_PC_PCP_20")
    df_costcomp_text.createOrReplaceTempView("0COSTCOMP_TEXT")
    df_product_masterdata.createOrReplaceTempView("product_master")

    df_std = spark.sql(PRICE_PROCESSING.STANDARD_COST.STANDARD_COST_QUERY)

    return df_std


def get_icp(
    df_a004: DataFrame,
    df_konp: DataFrame,
    df_product_masterdata: DataFrame,
) -> DataFrame:
    """
    ICP — joins A004 with KONP and product_master.

    Args:
        df_a004              : ICP condition table A004
        df_konp              : Condition header table KONP
        df_product_masterdata: Product masterdata (from PRODUCT_MASTERDATA process)

    Returns:
        DataFrame: Final ICP
    """

    # ── Register temp views ───────────────────────────────────────────────────
    df_a004.createOrReplaceTempView("A004")
    df_konp.createOrReplaceTempView("KONP")
    df_product_masterdata.createOrReplaceTempView("product_master")

    df_icp = spark.sql(PRICE_PROCESSING.ICP.ICP_QUERY)

    return df_icp
