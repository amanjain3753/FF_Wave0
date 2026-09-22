from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager

from mwd30anaplan.data_engineering.data_processing.constants import (
    MASTERDATA_PROCESSING,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_price import (
    get_customer_price_list,
    get_icp,
    get_standard_cost,
)


@logger
def customer_price_list_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Customer Price List processing.
    Reads 9 SAP condition tables + product_master + customer_master.
    """
    df_dict = jobDAO.data_dict

    LoggingManager().get_logger().info(
        f"Customer Price List process started. Process date: {process_date}"
    )

    df_customer_price_list = get_customer_price_list(
        df_dict["df_a501"],
        df_dict["df_a812"],
        df_dict["df_a872"],
        df_dict["df_a865"],
        df_dict["df_a883"],
        df_dict["df_a882"],
        df_dict["df_a513"],
        df_dict["df_a599"],
        df_dict["df_konp"],
        df_dict[
            MASTERDATA_PROCESSING.PRODUCT_MASTERDATA.PRODUCT_MASTERDATA_ANAPLAN
        ],  # df_product_masterdata
        df_dict[
            MASTERDATA_PROCESSING.CUSTOMER_MASTERDATA.CUSTOMER_MASTERDATA_ANAPLAN
        ],  # df_customer_masterdata
        df_dict["df_edf_latam_csl_pricing_info"],
    )

    LoggingManager().get_logger().info("Customer Price after feature")
    df_dict["df_customer_price_list"] = df_customer_price_list

    LoggingManager().get_logger().info("Customer Price List process completed.")
    return df_dict


@logger
def standard_cost_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Standard Cost processing.
    Reads ZBW_CO_PC_PCP_20 + 0COSTCOMP_TEXT + product_master.
    """
    df_dict = jobDAO.data_dict

    LoggingManager().get_logger().info(
        f"Standard Cost process started. Process date: {process_date}"
    )

    df_standard_cost = get_standard_cost(
        df_dict["df_zbw_co_pc_pcp_20"],
        df_dict["df_costcomp_text"],
        df_dict[
            MASTERDATA_PROCESSING.PRODUCT_MASTERDATA.PRODUCT_MASTERDATA_ANAPLAN
        ],  # df_product_masterdata
    )

    LoggingManager().get_logger().info("Standard Cost ")

    df_dict["df_standard_cost"] = df_standard_cost

    LoggingManager().get_logger().info("Standard Cost process completed.")
    return df_dict


@logger
def icp_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: ICP processing.
    Reads A004 + KONP (reused from price list) + product_master.
    """
    df_dict = jobDAO.data_dict

    LoggingManager().get_logger().info(
        f"ICP process started. Process date: {process_date}"
    )

    df_icp = get_icp(
        df_dict["df_a004"],
        df_dict["df_konp"],  # reused from CUSTOMER_PRICE_LIST
        df_dict[
            MASTERDATA_PROCESSING.PRODUCT_MASTERDATA.PRODUCT_MASTERDATA_ANAPLAN
        ],  # df_product_masterdata
    )

    LoggingManager().get_logger().info("ICP row")
    df_dict["df_icp"] = df_icp

    LoggingManager().get_logger().info("ICP process completed.")
    return df_dict
