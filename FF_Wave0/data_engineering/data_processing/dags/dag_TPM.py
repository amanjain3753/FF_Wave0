from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager

from mwd30anaplan.data_engineering.data_processing.constants import TPM_PROCESSING
from mwd30anaplan.data_engineering.data_processing.feature.common_functions import (
    get_forward_fiscal_year_periods,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_TPM import get_TPM


@logger
def tpm_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Trade Promo Management (TPM) processing.
    Reads TPM silver tables (fact_account_plan, dim_cust_sales, dim_material,
    dim_calendar_tpm) and manual CCA/MX files to build unified trade promo
    output for Anaplan. CA (salesorg 121) trade is calculated inline via CTEs.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution.

    Returns:
        dict: Updated data_dict with trade promo DataFrame.
    """
    df_dict = jobDAO.data_dict

    LoggingManager().get_logger().info(
        f"TPM process started. Process date: {process_date}"
    )

    df_trade_promo = get_TPM(
        df_dict["df_fact_account_plan"],
        df_dict["df_dim_cust_sales"],
        df_dict["df_dim_material"],
        df_dict["df_dim_calendar_tpm"],
        df_dict["df_fact_internal_product_week"],
        df_dict["df_dim_manual_kpis"],
    )

    periods = get_forward_fiscal_year_periods(
        df_trade_promo, jobDAO, process_name="TPM"
    )
    if periods:
        df_trade_promo = df_trade_promo.filter(
            df_trade_promo["Fiscal_year_period"].isin(periods)
        )

    df_dict[TPM_PROCESSING.TPM_PROCESSING_OUTPUT] = df_trade_promo

    LoggingManager().get_logger().info("TPM process completed.")
    return df_dict
