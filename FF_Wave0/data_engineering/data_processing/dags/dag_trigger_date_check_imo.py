import json

from pyspark.sql import SparkSession
from simpel.interface.dao import IJobDAO
from simpel.utils.db_utils import get_dbutils

from mwd30anaplan.data_engineering.data_processing.feature.feature_trigger_date_check_imo import (
    update_task_values,
    update_task_values_actuals,
    get_anchor_period_info,
    previous_year_period,
)

spark = SparkSession.builder.getOrCreate()
dbutils = get_dbutils(spark)


def trigger_date_check_imo(jobDAO: IJobDAO, process_date: str):
    """
    Determines refresh mode (manual or scheduled) and sets Databricks
    task parameters accordingly.

    This function:
    - Reads runtime arguments and calendar data from the Job DAO.
    - Identifies whether the job is triggered as a manual refresh
      or via a scheduled run.
    - For manual refreshes, propagates user-provided year-period
      parameters to downstream tasks.
    - For scheduled runs, derives refresh parameters from the
      Mars calendar and updates task values dynamically.

    Args:
        jobDAO (IJobDAO):
            Data access object providing logger, runtime arguments,
            and required calendar DataFrames.
        process_date (str):
            Processing date in 'YYYY-MM-DD' format used for
            orchestration and audit context.

    Returns:
        None
    """
    logger = jobDAO.logger
    df_dict = jobDAO.data_dict
    df_mars_calander = df_dict["mars_cal"]
    logger.info("Args:")
    logger.info(jobDAO.args)
    is_refresh_day = jobDAO.args.get("is_refresh_day") or ""
    year_period_list = jobDAO.args.get("year_period_list") or ""
    process_date_raw = jobDAO.env_config_dict.get("process_date_value") or ""
    # reformat "20260817" -> "2026-08-17"
    if process_date_raw and len(process_date_raw) == 8:
        process_date = (
            f"{process_date_raw[0:4]}-{process_date_raw[4:6]}-{process_date_raw[6:8]}"
        )
    else:
        process_date = process_date_raw
    parameters = {
        "is_refresh_day": is_refresh_day,
        "year_period_list": year_period_list,
    }
    logger.info(f"Parameters: {parameters}")

    if year_period_list:
        logger.info("Running Manual Refresh")
        dbutils.jobs.taskValues.set("is_refresh_day", True)
        dbutils.jobs.taskValues.set("process_date", process_date)  # <-- add this
        dbutils.jobs.taskValues.set("year_period_list", year_period_list)

        logger.info(f"type(year_period_list) = {type(year_period_list)}")
        logger.info(f"value(year_period_list) = {year_period_list}")
        logger.info(f"value(process_date) = {process_date}")

        dbutils.jobs.taskValues.set("year_period_list", year_period_list)
        
    elif str(is_refresh_day).strip().lower() == "true":
        anchor_date, year_period, _, _ = get_anchor_period_info(
            df_mars_calander, process_date, logger, anchor_weekday="TUESDAY"
        )
        forced_periods = [previous_year_period(int(year_period), logger)]
        dbutils.jobs.taskValues.set("is_refresh_day", True)
        dbutils.jobs.taskValues.set("process_date", anchor_date)
        dbutils.jobs.taskValues.set("year_period_list", json.dumps(forced_periods))
    else:
        logger.info("Running Scheduled Refresh")
        update_task_values(
            df_mars_calander,
            process_date,
            logger,
            jobDAO,
        )


def trigger_date_check_FF_actuals(jobDAO: IJobDAO, process_date: str):
    """
    Determines refresh mode and sets Databricks task parameters for the
    Actuals pipeline (anchored to W2 MONDAY, instead of W2 TUESDAY used by
    the Process pipeline's trigger_date_check_imo).

    Mirrors trigger_date_check_imo's structure exactly - same manual/
    scheduled branching - just calls update_task_values_actuals instead
    of update_task_values.

    Args:
        jobDAO (IJobDAO):
            Data access object providing logger, runtime arguments,
            and required calendar DataFrames.
        process_date (str):
            Processing date in 'YYYY-MM-DD' format used for
            orchestration and audit context.

    Returns:
        None
    """
    logger = jobDAO.logger
    df_dict = jobDAO.data_dict
    df_mars_calander = df_dict["mars_cal"]
    logger.info("Args:")
    logger.info(jobDAO.args)
    is_refresh_day = jobDAO.args.get("is_refresh_day") or ""
    year_period_list = jobDAO.args.get("year_period_list") or ""
    process_date_raw = jobDAO.env_config_dict.get("process_date_value") or ""
    if process_date_raw and len(process_date_raw) == 8:
        process_date = (
            f"{process_date_raw[0:4]}-{process_date_raw[4:6]}-{process_date_raw[6:8]}"
        )
    else:
        process_date = process_date_raw
    parameters = {
        "is_refresh_day": is_refresh_day,
        "year_period_list": year_period_list,
    }
    logger.info(f"Parameters: {parameters}")
    
    if year_period_list:
        logger.info("Running Manual Refresh (Actuals)")
        dbutils.jobs.taskValues.set("is_refresh_day", True)
        dbutils.jobs.taskValues.set("process_date", process_date)
        dbutils.jobs.taskValues.set("year_period_list", year_period_list)

    elif str(is_refresh_day).strip().lower() == "true":
        anchor_date, year_period, _, _ = get_anchor_period_info(
            df_mars_calander, process_date, logger, anchor_weekday="MONDAY"
        )
        forced_periods = [previous_year_period(int(year_period), logger)]
        dbutils.jobs.taskValues.set("is_refresh_day", True)
        dbutils.jobs.taskValues.set("process_date", anchor_date)
        dbutils.jobs.taskValues.set("year_period_list", json.dumps(forced_periods))
    else:
        logger.info("Running Scheduled Refresh (Actuals)")
        update_task_values_actuals(
            df_mars_calander,
            process_date,
            logger,
            jobDAO,
        )