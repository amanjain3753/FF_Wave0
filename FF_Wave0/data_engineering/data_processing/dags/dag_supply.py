from pyspark.sql import SparkSession
from simpel.decorator.log import logger
from simpel.interface.dao import IJobDAO
from simpel.logger.logging import LoggingManager
from simpel.utils.db_utils import get_dbutils

from mwd30anaplan.data_engineering.data_processing.constants import SUPPLY_PROCESSING
from mwd30anaplan.data_engineering.data_processing.feature.common_functions import (
    get_forward_fiscal_year_periods,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_supply import (
    get_supply_all,
)

spark = SparkSession.builder.getOrCreate()
dbutils = get_dbutils(spark)


@logger
def supply_process(jobDAO: IJobDAO, process_date: str):
    """
    DAG: Supply All — Despatched (NA+LATAM) + Production (NA+LATAM).
    Reads Kinaxis supply/production tables and mapping files to build
    the unified supply output for Anaplan.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution.

    Returns:
        dict: Updated data_dict with supply DataFrame.
    """
    df_dict = jobDAO.data_dict

    # Pull the anchor date set by trigger_date_check, falling back to the
    # scheduler-supplied process_date if the task value isn't available
    # (e.g. local/unit-test runs where there's no upstream task).
    try:
        anchor_process_date = dbutils.jobs.taskValues.get(
            taskKey="trigger_date_check",
            key="process_date",
            default=process_date,
        )
    except Exception:
        anchor_process_date = process_date

    LoggingManager().get_logger().info(
        f"Supply All process started. Process date (anchor): {anchor_process_date}"
    )

    df_supply = get_supply_all(
        df_dict["df_despatched"],
        df_dict["df_production_unit"],
        df_dict["df_production_tonnes"],
        df_dict["df_latam"],
        df_dict["df_mars_calendar"],
        df_dict["df_uom"],
        df_dict["df_salesorg"],
        df_dict["df_material_master"],
        anchor_process_date,
    )

    # get_forward_fiscal_year_periods looks up the Mars calendar under the
    # fixed key "mars_cal"; reuse the already-loaded df_mars_calendar instead
    # of adding a duplicate input for the same table.
    df_dict["mars_cal"] = df_dict["df_mars_calendar"]
    periods = get_forward_fiscal_year_periods(df_supply, jobDAO, process_name="SUPPLY")
    if periods:
        df_supply = df_supply.filter(df_supply["Fiscal_year_period"].isin(periods))

    df_dict[SUPPLY_PROCESSING.SUPPLY_OUTPUT] = df_supply

    LoggingManager().get_logger().info("Supply All process completed.")
    return df_dict
