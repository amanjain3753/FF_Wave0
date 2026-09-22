import json

from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager

from mwd30anaplan.data_engineering.data_processing.constants import ACTUALS_RAW
from mwd30anaplan.data_engineering.data_processing.feature.feature_actuals_raw import (
    get_actuals_raw,
)


@logger
def actuals_raw_process(jobDAO: IJobDAO, process_date: str):
    """
    Materialise the filtered source facts into the RAW zone consumed by
    ACTUALS_PROCESS.

    This process must complete before ACTUALS_PROCESS runs, because
    ACTUALS_PROCESS reads its ``facts_financial_consolidated_customer`` and
    ``ep_account_entity`` inputs directly from the RAW parquet locations written
    by the file_writer `output` entries of ACTUALS_RAW_PROCESS in
    project_config.json (paths, partition columns and dynamic-overwrite mode all
    live in that config).

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and
            data_dict.
        process_date (str): Date of process execution.

    Returns:
        dict: The data_dict with the two RAW DataFrames added under the output
            names the framework writes (ACTUALS_RAW.CUSTOMER_OUTPUT / EP_OUTPUT).
    """

    df_dict = jobDAO.data_dict
    LoggingManager().get_logger().info(
        f"Actuals RAW process started. Process date: {process_date}"
    )

    year_period_list = jobDAO.args.get("year_period_list")
    if not year_period_list:
        raise ValueError("year_period_list is required for ACTUALS_RAW")

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

    LoggingManager().get_logger().info(
        f"Actuals RAW year_period_list: {year_period_list}"
    )

    df_customer_raw, df_ep_raw = get_actuals_raw(
        df_facts_source=df_dict["facts_financial_consolidated_customer_src"],
        df_ep_source=df_dict["ep_account_entity_src"],
        df_ac_id_filters=df_dict["df_ac_id_filters"],
        df_entity_id_filter=df_dict["df_entity_id_filter"],
        year_period_list=year_period_list,
    )

    # Hand the RAW DataFrames back to the framework, which writes each one to its
    # configured RAW parquet destination (write_path + partition_columns +
    # dynamic overwrite) declared in ACTUALS_RAW_PROCESS.output.
    df_dict[ACTUALS_RAW.CUSTOMER_OUTPUT] = df_customer_raw
    df_dict[ACTUALS_RAW.EP_OUTPUT] = df_ep_raw

    LoggingManager().get_logger().info("Actuals RAW process completed.")
    return df_dict
