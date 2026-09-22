from pyspark.sql import DataFrame, SparkSession
from simpel.utils.db_utils import get_dbutils

from mwd30anaplan.data_engineering.data_processing.constants import (
    MASTERDATA_PROCESSING,
)

spark = SparkSession.builder.getOrCreate()
dbutils = get_dbutils(spark)


def get_customer_masterdata(
    df_customer_attr: DataFrame,
    df_customer_text: DataFrame,
    df_cust_sales_attr: DataFrame,
    df_custopf_attr: DataFrame,
) -> DataFrame:
    """
    Customer Masterdata — joins 4 SAP source tables.

    Args:
        df_customer_attr   : Customer attributes (0CUSTOMER_ATTR)
        df_customer_text   : Customer text/description (0CUSTOMER_TEXT)
        df_cust_sales_attr : Customer sales attributes (0CUST_SALES_ATTR)
        df_custopf_attr    : Customer partner functions (ZCUSTOPF_ATTR)

    Returns:
        DataFrame: Final Customer Masterdata
    """
    df_customer_attr.createOrReplaceTempView("0CUSTOMER_ATTR")
    df_customer_text.createOrReplaceTempView("0CUSTOMER_TEXT")
    df_cust_sales_attr.createOrReplaceTempView("0CUST_SALES_ATTR")
    df_custopf_attr.createOrReplaceTempView("ZCUSTOPF_ATTR")

    df_customer = spark.sql(
        MASTERDATA_PROCESSING.CUSTOMER_MASTERDATA.CUSTOMER_MASTERDATA_QUERY
    )

    return df_customer


def get_product_masterdata(
    df_material_attr: DataFrame,
    df_material_text: DataFrame,
    df_zbrand_text: DataFrame,
    df_zbrands_text: DataFrame,
    df_zclf01_text: DataFrame,
    df_zclf20_text: DataFrame,
    df_zclf10_text: DataFrame,
    df_zclf17_text: DataFrame,
    df_zclf18_text: DataFrame,
    df_zclf21_text: DataFrame,
    df_dimensions_item_taxonomy: DataFrame,
    df_dimensions_vw_item_product_category: DataFrame,
    df_dimensions_it_product_pack_size: DataFrame,
    df_dimensions_it_product_category: DataFrame,
    df_dimensions_it_ec_group: DataFrame,
) -> DataFrame:
    """
    Product Masterdata — joins 10 SAP tables + 5 catalog tables.
    """
    df_material_attr.createOrReplaceTempView("0MATERIAL_ATTR")
    df_material_text.createOrReplaceTempView("0MATERIAL_TEXT")
    df_zbrand_text.createOrReplaceTempView("ZBRAND_TEXT")
    df_zbrands_text.createOrReplaceTempView("ZBRANDS_TEXT")
    df_zclf01_text.createOrReplaceTempView("ZCLF01_TEXT")
    df_zclf20_text.createOrReplaceTempView("ZCLF20_TEXT")
    df_zclf10_text.createOrReplaceTempView("ZCLF10_TEXT")
    df_zclf17_text.createOrReplaceTempView("ZCLF17_TEXT")
    df_zclf18_text.createOrReplaceTempView("ZCLF18_TEXT")
    df_zclf21_text.createOrReplaceTempView("ZCLF21_TEXT")
    df_dimensions_item_taxonomy.createOrReplaceTempView("dimensions_item_taxonomy")
    df_dimensions_vw_item_product_category.createOrReplaceTempView(
        "dimensions_vw_item_product_category"
    )
    df_dimensions_it_product_pack_size.createOrReplaceTempView(
        "dimensions_it_product_pack_size"
    )
    df_dimensions_it_product_category.createOrReplaceTempView(
        "dimensions_it_product_category"
    )
    df_dimensions_it_ec_group.createOrReplaceTempView("dimensions_it_ec_group")

    df_product = spark.sql(
        MASTERDATA_PROCESSING.PRODUCT_MASTERDATA.PRODUCT_MASTERDATA_QUERY
    )

    return df_product
