from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager

from mwd30anaplan.data_engineering.data_processing.constants import UOM_PROCESSING
from mwd30anaplan.data_engineering.data_processing.feature.feature_uom import get_uom


@logger
def uom_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: UOM processing.
    Reads material unit conversions + product masterdata and writes UOM mapping.
    """
    df_dict = jobDAO.data_dict

    LoggingManager().get_logger().info(
        f"UOM process started. Process date: {process_date}"
    )

    df_uom = get_uom(
        df_dict["df_material_unit_conversions"], df_dict["product_masterdata_anaplan"]
    )

    LoggingManager().get_logger().info("UOM row after feature function")

    df_dict[UOM_PROCESSING.UOM_OUTPUT] = df_uom

    LoggingManager().get_logger().info("UOM process completed.")
    return df_dict
