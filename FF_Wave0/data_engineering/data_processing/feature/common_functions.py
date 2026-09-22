import re

from pyspark.sql import functions as F
from simpel.interface.dao import IJobDAO

from mwd30anaplan.data_engineering.data_processing.feature.feature_trigger_date_check_imo import (
    get_anchor_period_info,
    previous_year_period,
)
from mwd30anaplan.data_engineering.data_processing.constants import (
PROCESSING_CONST as const
)

def _fiscal_period_year(value):
    """
    Extract the 4-digit fiscal year from a fiscal-year-period value.

    The TPM data uses the format 'P8 FY26', where the two digits after 'FY' are
    the last two digits of the year: 'FY26' -> 2026, 'FY27' -> 2027.

    Returns None when no year can be parsed.
    """
    text = str(value).strip()
    marker = text.upper().rfind("FY")
    if marker != -1:
        suffix = text[marker + 2 :].strip()[:2]
        if suffix.isdigit():
            return 2000 + int(suffix)
    return None


def _fiscal_period_number(value):
    """
    Extract the period number from a fiscal-year-period value.

    'P8 FY26' -> 8. Returns None when no valid period number (1..13) is found.
    """
    match = re.match(r"^\s*P\s*(\d{1,2})", str(value).strip().upper())
    if match:
        number = int(match.group(1))
        if 1 <= number <= const.MARS_PERIODS_PER_YEAR:
            return number
    return None


def _period_index(value):
    """
    Turn a fiscal-year-period value into an absolute, comparable period index.

    'P8 FY26' -> 2026 * 13 + 7. Consecutive periods differ by 1, so the index
    rolls over the fiscal-year boundary on its own ('P13 FY26' + 1 == 'P1 FY27').
    Returns None when the value cannot be parsed.
    """
    year = _fiscal_period_year(value)
    number = _fiscal_period_number(value)
    if year is None or number is None:
        return None
    return year * const.MARS_PERIODS_PER_YEAR + (number - 1)


def _period_label(index):
    """Inverse of _period_index: 2026 * 13 + 7 -> 'P8 FY26'."""
    year, offset = divmod(index, const.MARS_PERIODS_PER_YEAR)
    return f"P{offset + 1} FY{year % 100:02d}"


def _current_mars_period_index(jobDAO: IJobDAO):
    """
    Resolve the Mars period we are currently in, as a period index.

    The Mars calendar (MAPPING_FILES/Mars_Cal.csv, exposed in data_dict as
    'mars_cal') is the same source trigger_date_check_imo uses. The latest calendar
    row on or before today wins, so a calendar without a row for today (weekend
    or holiday gap) still resolves to the right period.

    Raises:
        ValueError: when the calendar is missing, malformed, or does not cover
            today. Failing here is deliberate - a wrong anchor would silently
            push the wrong 18 periods to Anaplan.
    """
    df_dict = getattr(jobDAO, "data_dict", None) or {}
    calendar = df_dict.get(const.MARS_CALENDAR_DF)
    if calendar is None:
        raise ValueError(
            f"Mars calendar DataFrame '{const.MARS_CALENDAR_DF}' not found in data_dict; "
            "add it to the process input config to derive the forward period window."
        )

    date_col = next((c for c in calendar.columns if c.lower() == "date"), None)
    period_col = next(
        (c for c in calendar.columns if c.lower() == "marsyearperiodnumeric"), None
    )
    if date_col is None or period_col is None:
        raise ValueError(
            "Mars calendar must expose 'Date' and 'MarsYearPeriodNumeric' columns; "
            f"found: {calendar.columns}"
        )

    rows = (
        calendar.select(
            F.coalesce(
                F.to_date(F.col(date_col), "M/d/yyyy"),
                F.to_date(F.col(date_col), "yyyy-MM-dd"),
                F.to_date(F.col(date_col)),
            ).alias("cal_date"),
            F.col(period_col).cast("int").alias("year_period"),
        )
        .where(
            F.col("cal_date").isNotNull()
            & F.col("year_period").isNotNull()
            & (F.col("cal_date") <= F.current_date())
        )
        .orderBy(F.col("cal_date").desc())
        .limit(1)
        .collect()
    )
    if not rows:
        raise ValueError(
            "Mars calendar has no row on or before today; cannot resolve the "
            "current Mars period."
        )

    year_period = int(rows[0]["year_period"])
    year, period = year_period // 100, year_period % 100
    if not 1 <= period <= const.MARS_PERIODS_PER_YEAR:
        raise ValueError(
            f"Unexpected MarsYearPeriodNumeric value '{year_period}' in the Mars calendar."
        )
    return year * const.MARS_PERIODS_PER_YEAR + (period - 1)


def get_forward_fiscal_year_periods(
    df, jobDAO: IJobDAO, periods_ahead=const.FORWARD_PERIODS_AHEAD, process_name="UNKNOWN"
):
    """
    Build the list of fiscal-year-period values to load for the forward looking
    assets (TPM, Supply, Demand).

    The window is the current Mars period plus the next ``periods_ahead``
    periods - 18 periods in total by default - and it rolls over fiscal years:
    with the current period at 'P8 FY26' the window ends at 'P12 FY27'.
    Anything before the current period is dropped, and periods inside the window
    that have no rows in the DataFrame simply do not appear in the result.

    The period column is resolved case-insensitively (it is 'Fiscal_year_period'
    in the TPM/Supply/Demand DataFrames) and the returned values are the
    DataFrame's own strings, sorted chronologically, so the caller can filter on
    equality.

    Args:
        df           : DataFrame expected to contain a fiscal-year-period column.
        jobDAO       : Job DAO; supplies the logger and the 'mars_cal' DataFrame.
        periods_ahead: How many periods after the current one to include.

    Returns:
        Chronologically sorted list of period strings to load, or None when the
        DataFrame has no fiscal-year-period column (so the caller falls back to
        a full load instead of failing).
    """
    logger = jobDAO.logger if jobDAO is not None else None

    period_col = next(
        (c for c in df.columns if c.lower() == "fiscal_year_period"), None
    )
    if period_col is None:
        if logger:
            logger.warning(
                "DataFrame has no fiscal-year-period column; cannot derive "
                "periods. Falling back to full load (distinct_period=None)."
            )
        return None

    start_index = _current_mars_period_index(jobDAO)
    end_index = start_index + periods_ahead
    if logger:
        logger.info(
            f"[{process_name}] [get_forward_fiscal_year_periods] window: "
            f"{_period_label(start_index)} .. {_period_label(end_index)} "
            f"({periods_ahead + 1} periods)"
        )

    in_window = {}
    for row in df.select(period_col).distinct().collect():
        value = row[period_col]
        if value is None:
            continue
        index = _period_index(value)
        if index is not None and start_index <= index <= end_index:
            in_window[index] = str(value)

    periods = [in_window[index] for index in sorted(in_window)]

    if logger:
        logger.info(f"[get_forward_fiscal_year_periods] selected periods: {periods}")
        missing = [
            _period_label(index)
            for index in range(start_index, end_index + 1)
            if index not in in_window
        ]
        if missing:
            logger.info(f"Periods in the window with no data (skipped): {missing}")
        if not periods:
            logger.warning(
                "No fiscal-year-period values fall inside the forward window; "
                "nothing will be filtered for load."
            )

        logger.info(
            f"[{process_name}] [get_forward_fiscal_year_periods] "
            f"{periods_ahead + 1}-period window -> periods={periods}"
        )
    return periods


def get_previous_fiscal_year_period(jobDAO: IJobDAO):
    """
    Resolve the previous fiscal period (P-1) as a distinct-period label list.

    The run date is read from ``jobDAO.env_config_dict['process_date_value']``
    - not passed in - so its format always matches the Mars calendar ('mars_cal'
    in data_dict). It is looked up in the calendar to get the current period,
    and ``previous_year_period`` steps one period back. This is the same
    resolution the trigger date check performs.

    ``previous_year_period`` returns a numeric period (``202608``) while
    fiscal-year-period columns are typically stored as a string
    (``'P8 FY26'``), so the value is converted before it is returned.

    Args:
        jobDAO: Job DAO providing 'mars_cal' in data_dict, env_config_dict and
            logger.

    Returns:
        list[str]: single-element list with the P-1 period label, e.g.
        ``['P8 FY26']``.

    Raises:
        ValueError: When the run date is missing from env_config_dict, or
            when it cannot be resolved against the Mars calendar (propagated
            from ``get_anchor_period_info``).
    """
    logger = jobDAO.logger
    df_mars_calander = jobDAO.data_dict[const.MARS_CALENDAR_DF]

    # Same normalisation the trigger date check does: the framework hands over
    # "20260831" but the Mars calendar Date column is "2026-08-31".
    process_date_raw = str(jobDAO.env_config_dict.get("process_date_value") or "")
    if len(process_date_raw) == 8:
        run_date = (
            f"{process_date_raw[0:4]}-{process_date_raw[4:6]}-{process_date_raw[6:8]}"
        )
    else:
        run_date = process_date_raw

    if not run_date:
        raise ValueError(
            "process_date_value is missing from env_config_dict; cannot resolve "
            "the fiscal period to upload."
        )

    _, year_period, _, _ = get_anchor_period_info(df_mars_calander, run_date, logger)
    current_year_period = int(year_period)
    upload_year_period = previous_year_period(current_year_period, logger)

    # 202608 -> 'P8 FY26', matching how Fiscal_Year_Period is built upstream.
    distinct_period = [
        f"P{upload_year_period % 100} FY{upload_year_period // 100 % 100:02d}"
    ]
    logger.info(
        f"Previous fiscal period resolved: run_date={run_date}, "
        f"current={current_year_period}, P-1={upload_year_period} -> {distinct_period}"
    )
    return distinct_period


def get_distinct_fiscal_year_periods(df):
    """
    Sorted list of the fiscal-year-period values already present in df.

    Used for the Anaplan push of TPM/Supply/Demand once the DataFrame has
    already been filtered to the 18-period window at write time - no calendar
    lookup needed here, just the periods that made it into df, in chronological
    order (plain string sort breaks at the FY rollover, e.g. 'P10 FY26' <
    'P2 FY26'). Returns None when df has no fiscal-year-period column.
    """
    period_col = next(
        (c for c in df.columns if c.lower() == "fiscal_year_period"), None
    )
    if period_col is None:
        return None

    return sorted(
        {
            str(row[period_col])
            for row in df.select(period_col).distinct().collect()
            if row[period_col] is not None
        },
        key=_period_index,
    )
