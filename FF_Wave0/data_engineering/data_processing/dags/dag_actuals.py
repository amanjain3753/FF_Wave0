import json

from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager

from mwd30anaplan.data_engineering.data_processing.constants import ACTUALS_PROCESSING
from mwd30anaplan.data_engineering.data_processing.feature.feature_actuals import (
    get_actuals,
)


@logger
def actuals_process(jobDAO: IJobDAO, process_date: str):
    """
    Run Actuals pipeline combining Customer and EP actuals data.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution.

    Returns:
        dict: Updated data_dict with final actuals DataFrame.

    Raises:
        ValueError: If year_period_list is not provided in jobDAO.args.
    """
    df_dict = jobDAO.data_dict

    LoggingManager().get_logger().info(
        f"Actuals process started. Process date: {process_date}"
    )

    year_period_list = jobDAO.args.get("year_period_list")
    if not year_period_list:
        raise ValueError("year_period_list is required for ACTUALS")

    if isinstance(year_period_list, str):
        try:
            year_period_list = json.loads(year_period_list)
        except json.JSONDecodeError:
            year_period_list = [
                int(x.strip()) for x in year_period_list.split(",") if x.strip()
            ]
    # Separate `if`, not `elif`: a manual run passing a single bare period
    # ("202507") parses as an int rather than a list, so it still needs wrapping
    # after the branch above has run.
    if isinstance(year_period_list, int):
        year_period_list = [year_period_list]

    LoggingManager().get_logger().info(f"Actuals year_period_list: {year_period_list}")

    df_actuals = get_actuals(
        df_facts_financial_consolidated_customer=df_dict[
            "facts_financial_consolidated_customer"
        ],
        df_ep_account_entity=df_dict["ep_account_entity"],
        df_dimension_entity=df_dict["dimensions_Entity"],
        df_dimensions_account=df_dict["dimensions_Account"],
        df_dimensions_item_taxonomy=df_dict["dimensions_Item_Taxonomy"],
        df_dimensions_currency=df_dict["dimensions_currency"],
        df_dimensions_customer=df_dict["dimensions_customer"],
        df_product=df_dict["df_product"],
        df_customer_master=df_dict["df_customer_master"],
        df_ac_id_filters=df_dict["df_ac_id_filters"],
        df_entity_id_filter=df_dict["df_entity_id_filter"],
        year_period_list=year_period_list,
    )

    df_dict[ACTUALS_PROCESSING.ACTUALS_OUTPUT] = df_actuals

    LoggingManager().get_logger().info("Actuals process completed.")
    return df_dict
