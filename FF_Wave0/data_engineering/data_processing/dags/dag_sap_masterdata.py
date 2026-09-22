from simpel.interface.dao import IJobDAO

from mwd30anaplan.data_engineering.data_processing.constants import (
    MASTERDATA_PROCESSING,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_sap_masterdata import (
    get_customer_masterdata,
    get_product_masterdata,
)


def customer_masterdata_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Customer Masterdata processing.
    Reads SAP customer attribute, text, sales, and partner function tables
    and builds the unified customer masterdata for Anaplan.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution.

    Returns:
        dict: Updated data_dict with customer masterdata DataFrame.
    """
    logger = jobDAO.logger
    df_dict = jobDAO.data_dict

    logger.info(f"Customer Masterdata process started. Process date: {process_date}")

    df_customer_masterdata = get_customer_masterdata(
        df_dict["df_customer_attr"],
        df_dict["df_customer_text"],
        df_dict["df_cust_sales_attr"],
        df_dict["df_custopf_attr"],
    )

    logger.info("Customer Masterdata after feature func runs")
    df_dict[
        MASTERDATA_PROCESSING.CUSTOMER_MASTERDATA.CUSTOMER_MASTERDATA_ANAPLAN
    ] = df_customer_masterdata

    logger.info("Customer Masterdata process completed.")
    return df_dict


def product_masterdata_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Product Masterdata processing.
    Reads SAP material attribute, text, brand, classification tables
    and finance item taxonomy dimensions to build unified product masterdata for Anaplan.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution.

    Returns:
        dict: Updated data_dict with product masterdata DataFrame.
    """
    logger = jobDAO.logger
    df_dict = jobDAO.data_dict

    logger.info(f"Product Masterdata process started. Process date: {process_date}")

    df_product_masterdata = get_product_masterdata(
        df_dict["df_material_attr"],
        df_dict["df_material_text"],
        df_dict["df_zbrand_text"],
        df_dict["df_zbrands_text"],
        df_dict["df_zclf01_text"],
        df_dict["df_zclf20_text"],
        df_dict["df_zclf10_text"],
        df_dict["df_zclf17_text"],
        df_dict["df_zclf18_text"],
        df_dict["df_zclf21_text"],
        df_dict["dimensions_item_taxonomy"],
        df_dict["dimensions_vw_item_product_category"],
        df_dict["dimensions_it_product_pack_size"],
        df_dict["dimensions_it_product_category"],
        df_dict["dimensions_it_ec_group"],
    )

    logger.info("Product Masterdata")
    df_dict[
        MASTERDATA_PROCESSING.PRODUCT_MASTERDATA.PRODUCT_MASTERDATA_ANAPLAN
    ] = df_product_masterdata

    logger.info("Product Masterdata process completed.")
    return df_dict
