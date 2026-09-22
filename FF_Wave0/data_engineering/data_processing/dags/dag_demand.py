from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager
from pyspark.sql import SparkSession
from simpel.utils.db_utils import get_dbutils

from mwd30anaplan.data_engineering.data_processing.constants import DEMAND_PROCESSING
from mwd30anaplan.data_engineering.data_processing.feature.common_functions import (
    get_forward_fiscal_year_periods,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_demand import (
    get_demand,
)

spark = SparkSession.builder.getOrCreate()
dbutils = get_dbutils(spark)


@logger
def demand_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Demand — NA forecast, LATAM consensus/pre-consensus and CCA combined
    into the unified demand output for Anaplan.
    Resolves the W2 Tuesday anchor published by trigger_date_check so every
    source locks to its newest snapshot on or before that date.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution; used as the anchor fallback
            when the trigger_date_check task value is unavailable.

    Returns:
        dict: Updated data_dict with demand DataFrame.
    """
    df_dict = jobDAO.data_dict
    try:
        anchor_process_date = dbutils.jobs.taskValues.get(
            taskKey="trigger_date_check",
            key="process_date",
            default=process_date,
        )
    except Exception:
        anchor_process_date = process_date

    LoggingManager().get_logger().info(
        f"Demand process started. Process date (anchor): {anchor_process_date}"
    )

    df_demand = get_demand(
        df_dict["df_comb_na"],
        df_dict["df_latm_consensus"],
        df_dict["df_latm_preconsensus"],
        df_dict["df_cca"],
        df_dict["df_mars_calendar"],
        df_dict["df_uom"],
        df_dict["df_salesorg"],
        df_dict["df_customer"],
        df_dict["df_product"],
        df_dict["df_forecast_mapping"],
        df_dict["df_bb_mapping"],
        df_dict["df_na_consensus"],
        anchor_process_date,
    )
    # get_forward_fiscal_year_periods looks up the Mars calendar under the
    # fixed key "mars_cal"; reuse the already-loaded df_mars_calendar instead
    # of adding a duplicate input for the same table.
    df_dict["mars_cal"] = df_dict["df_mars_calendar"]
    periods = get_forward_fiscal_year_periods(df_demand, jobDAO, process_name="DEMAND")
    if periods:
        df_demand = df_demand.filter(df_demand["Fiscal_year_period"].isin(periods))

    df_dict[DEMAND_PROCESSING.DEMAND_OUTPUT] = df_demand

    LoggingManager().get_logger().info("Demand process completed.")
    return df_dict
