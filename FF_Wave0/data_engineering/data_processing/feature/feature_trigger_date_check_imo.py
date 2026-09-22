from simpel.decorator.log import logger
from simpel.logger.logging import LoggingManager
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import col
from pyspark.sql import functions as F
from simpel.utils.db_utils import get_dbutils
from logging import Logger
import json
from simpel.interface.dao import IJobDAO
from datetime import datetime, date
from pyspark.sql import SparkSession

try:
    spark = SparkSession.builder.getOrCreate()
    dbutils = get_dbutils(spark)
except Exception:
    spark = None
    dbutils = None
@logger
def get_anchor_period_info(df_mars_cal, process_date, logger, anchor_weekday="TUESDAY"):
    """
    Resolve the marsyearperiod that process_date belongs to, and return the
    W2 TUESDAY anchor date + period info for that period (per reference SQL logic).

    Args:
        df_mars_cal (DataFrame): Mars GCalendar data.
        process_date (str | date): The date the pipeline is running for (from workflow).
        logger (Logger): Logger instance for logging info.

    Returns:
        tuple: (anchor_date: str, year_period: any, period_number: any, is_exact_trigger: bool)
    """
    if isinstance(process_date, (datetime, date)):
        process_date_str = process_date.strftime("%Y-%m-%d")
    else:
        process_date_str = str(process_date).strip()[:10]
        
    LoggingManager().get_logger().info(
        f"Raw process_date received: {process_date!r} -> normalized: {process_date_str}"
    )
    df = (
        df_mars_cal
        .withColumn("Date", F.to_date("Date", "M/d/yyyy"))
        .withColumn("Date", F.date_format("Date", "yyyy-MM-dd"))
    )
    process_date_str = str(process_date)

    # Step 1: find which period process_date belongs to
    period_row = (
        df.filter(F.col("Date") == process_date_str)
        .select("marsyearperiod")
        .collect()
    )

    if not period_row:
        raise ValueError(
            f"process_date {process_date_str} not found in Mars calendar; cannot resolve period."
        )

    mars_year_period = period_row[0]["marsyearperiod"]

    # Step 2: find the W2 TUESDAY anchor date for that period (reference logic)
    anchor_row = (
        df.filter(
            (F.col("marsyearperiod") == mars_year_period)
            & (F.col("weekinperiodname") == "W2")
            & (F.col("weekdayname") == anchor_weekday)
        )
        .collect()
    )

    if not anchor_row:
        raise ValueError(
            f"No W2 {anchor_weekday} anchor found in Mars calendar for period {mars_year_period}."
        )

    anchor = anchor_row[0]

    
    anchor_date = anchor["Date"]
    year_period = anchor["marsyearperiodnumeric"]
    period_number = anchor["periodnumber"]
    is_exact_trigger = process_date_str == anchor_date

    LoggingManager().get_logger().info(
        f"process_date={process_date_str}, resolved_period={mars_year_period}, "
        f"anchor_date(W2 {anchor_weekday})={anchor_date}, exact_match={is_exact_trigger}, "
        f"year_period={year_period}, period_number={period_number}"
    )

    return anchor_date, year_period, period_number, is_exact_trigger

@logger
def previous_year_period(yearperiod, logger):
    """
    Return the yearperiod one period before the given yearperiod.

    Args:
        yearperiod (int): e.g., 202408
        logger (Logger): Logger instance for logging info.

    Returns:
        int: previous yearperiod, e.g., 202407 or 202313 if input is 202401
    """

    year = int(yearperiod) // 100
    period = int(yearperiod) % 100

    if period > 1:
        period -= 1
    else:
        year -= 1
        period = 13
    previous_period = year * 100 + period
    LoggingManager().get_logger().info(
        f"Previous Period(Inside previous_year_period function): {previous_period}"
    )
    return previous_period


@logger
def get_custom_year_period_list(current_year_period, logger):
    """
    Generate year periods for last 5 years up to the current period.

    Logic:
    - Subtract 500 to get start year/period
    - Start year: start_period → 13
    - Intermediate years: 01 → 13
    - Current year: 01 → current_period

    Args:
        current_year_period (int): e.g., 202506
        logger (Logger): Logger instance for logging info.

    Returns:
        List[int]: list of YearPeriods
    """
    current_year = current_year_period // 100
    current_period = current_year_period % 100

    start_year_period = current_year_period - 500
    start_year = start_year_period // 100
    start_period = start_year_period % 100

    year_period_list = []

    for year in range(start_year, current_year + 1):
        if year == start_year:
            periods = range(start_period, 14)
        elif year == current_year:
            periods = range(1, current_period + 1)
        else:
            periods = range(1, 14)
        year_period_list.extend([year * 100 + p for p in periods])
    LoggingManager().get_logger().info(
        f"Year Period List Generated Successfully: {year_period_list}"
    )
    return year_period_list


@logger
def update_task_values(df_mars_calander, process_date, logger, jobDAO,anchor_weekday="TUESDAY"):
    """
    Resolve the trigger period for the given process_date and set Databricks
    job task values accordingly.
    """
    logger = jobDAO.logger
 
    logger.info(f"jobDAO.__dict__: {jobDAO.__dict__}")
 
    anchor_date, year_period, period_number, is_exact_trigger = get_anchor_period_info(
        df_mars_calander, process_date, logger, anchor_weekday=anchor_weekday
    )
 
    if is_exact_trigger:
        year_period_list = [previous_year_period(int(year_period), logger)]

        LoggingManager().get_logger().info(
            f"process_date {process_date} is the W2 {anchor_weekday} trigger date. "
            f"Setting is_refresh_day:True, year_period:{str(year_period_list)}"
        )

        dbutils.jobs.taskValues.set("is_refresh_day", True)
        dbutils.jobs.taskValues.set(
            "year_period_list", json.dumps(year_period_list)
        )
        dbutils.jobs.taskValues.set("process_date", anchor_date)
    else:
        LoggingManager().get_logger().info(
            f"process_date {process_date} is not the W2 {anchor_weekday} trigger date "
            f"(anchor for period {year_period} is {anchor_date}); skipping refresh."
        )
        dbutils.jobs.taskValues.set("is_refresh_day", False)
    
@logger
def update_task_values_actuals(df_mars_calander, process_date, logger, jobDAO):
    """
    Actuals-only wrapper around update_task_values, anchored to W2 MONDAY
    instead of the default W2 TUESDAY used by the Process pipeline.
    """
    update_task_values(
        df_mars_calander, process_date, logger, jobDAO, anchor_weekday="MONDAY"
    )