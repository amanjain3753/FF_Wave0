from pyspark.sql import DataFrame, SparkSession

from mwd30anaplan.data_engineering.data_processing.constants import UOM_PROCESSING

spark = SparkSession.builder.getOrCreate()


def get_uom(
    df_material_unit_conversions: DataFrame,
    df_product_masterdata: DataFrame,
) -> DataFrame:
    """
    UOM — joins material_unit_conversions with product_master.

    Args:
        df_material_unit_conversions: SAP material unit conversion table
        df_product_masterdata       : Product masterdata (from PRODUCT_MASTERDATA process)

    Returns:
        DataFrame: Final UOM mapping
    """

    # Register temp views
    df_material_unit_conversions.createOrReplaceTempView("material_unit_conversions")
    df_product_masterdata.createOrReplaceTempView("product_master")

    df_uom = spark.sql(UOM_PROCESSING.UOM_QUERY)

    return df_uom
