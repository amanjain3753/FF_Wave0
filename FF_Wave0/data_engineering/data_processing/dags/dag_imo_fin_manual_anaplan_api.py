from simpel.interface.dao import IJobDAO

from mwd30anaplan.data_engineering.data_processing.constants import (
    ANAPLAN_API_PROCESS,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_imo_anaplan import (
    imo_fin_run_anaplan_process,
    imo_fin_run_anaplan_process_actuals,
)
from mwd30anaplan.data_engineering.data_processing.feature.common_functions import (
    get_distinct_fiscal_year_periods,
    get_previous_fiscal_year_period,
)

# Data assets that can be pushed manually to the IMO Fin Anaplan model.
# Each entry maps the --dataframe job parameter to:
#   "config"          : the ANAPLAN_API_PROCESS class holding the Anaplan ids and input df name
#   "period_based"    : True when the upload is split per Fiscal_Year_Period, False for full loads
#   "period_selector" : how the periods are derived from df when no year_period_list is
#                       passed, called as (df,); the forward looking assets (already
#                       filtered to the 18-period window at write time) just take the
#                       periods present in df. None for the full-load assets and for
#                       actuals, which instead resolves the previous fiscal period (P-1)
#                       via get_previous_fiscal_year_period - see
#                       imo_fin_manual_anaplan_api_process.
#   "uploader"        : the feature function used to push the data
IMO_FIN_MANUAL_ASSETS = {
    "actuals": {
        "config": ANAPLAN_API_PROCESS.ACTUALS_NEW,
        "period_based": True,
        "period_selector": None,
        "uploader": imo_fin_run_anaplan_process_actuals,
    },
    "tpm": {
        "config": ANAPLAN_API_PROCESS.TPM,
        "period_based": True,
        "period_selector": get_distinct_fiscal_year_periods,
        "uploader": imo_fin_run_anaplan_process,
    },
    "supply": {
        "config": ANAPLAN_API_PROCESS.SUPPLY,
        "period_based": True,
        "period_selector": get_distinct_fiscal_year_periods,
        "uploader": imo_fin_run_anaplan_process,
    },
    "demand": {
        "config": ANAPLAN_API_PROCESS.DEMAND,
        "period_based": True,
        "period_selector": get_distinct_fiscal_year_periods,
        "uploader": imo_fin_run_anaplan_process,
    },
    "customer_masterdata": {
        "config": ANAPLAN_API_PROCESS.CUSTOMER_MASTERDATA,
        "period_based": False,
        "period_selector": None,
        "uploader": imo_fin_run_anaplan_process,
    },
    "product_masterdata": {
        "config": ANAPLAN_API_PROCESS.PRODUCT_MASTERDATA,
        "period_based": False,
        "period_selector": None,
        "uploader": imo_fin_run_anaplan_process,
    },
    "customer_price_list": {
        "config": ANAPLAN_API_PROCESS.CUSTOMER_PRICE_LIST,
        "period_based": False,
        "period_selector": None,
        "uploader": imo_fin_run_anaplan_process,
    },
    "standard_cost": {
        "config": ANAPLAN_API_PROCESS.STANDARD_COST,
        "period_based": False,
        "period_selector": None,
        "uploader": imo_fin_run_anaplan_process,
    },
    "icp": {
        "config": ANAPLAN_API_PROCESS.ICP,
        "period_based": False,
        "period_selector": None,
        "uploader": imo_fin_run_anaplan_process,
    },
}


def imo_fin_manual_anaplan_api_process(jobDAO: IJobDAO, process_date: str):
    """
    Manually push one IMO Fin data asset to Anaplan.

    Driven by two job parameters:
        --dataframe        : which asset to upload, one of IMO_FIN_MANUAL_ASSETS
                             (actuals, tpm, supply, demand, customer_masterdata,
                             product_masterdata, customer_price_list,
                             standard_cost, icp).
        --year_period_list : comma separated Fiscal_Year_Period values, e.g.
                             "P4 FY26,P5 FY26". Only used for period based
                             assets. When it is empty the periods are derived
                             the same way the scheduled driver pipeline does:
                             actuals resolve the previous fiscal period (P-1)
                             from process_date via the Mars calendar, while
                             tpm, supply and demand take whatever periods are
                             present in df (already limited to the 18-period
                             window when it was written to ADLS).

    Masterdata and price assets are always full loads, so the period list is
    ignored for them.

    Args:
        jobDAO (IJobDAO): Job data access object containing args, logger, and data_dict.
        process_date (str): Date of process execution.

    Returns:
        None
    """
    logger = jobDAO.logger
    df_dict = jobDAO.data_dict

    data_asset = (jobDAO.args.get("dataframe") or "").strip().lower()
    year_period_list = jobDAO.args.get("year_period_list")

    if data_asset not in IMO_FIN_MANUAL_ASSETS:
        raise ValueError(
            f"Unknown dataframe '{data_asset}' for IMO_FIN_MANUAL_UPLOAD. "
            f"Expected one of: {sorted(IMO_FIN_MANUAL_ASSETS)}"
        )

    asset = IMO_FIN_MANUAL_ASSETS[data_asset]
    config = asset["config"]
    df = df_dict[config.INPUT_DF]

    requested_periods = []
    if isinstance(year_period_list, str):
        requested_periods = [
            x.strip() for x in year_period_list.split(",") if x.strip()
        ]

    if not asset["period_based"]:
        distinct_period = None
        if requested_periods:
            logger.info(
                f"'{data_asset}' is a full load asset; ignoring year_period_list "
                f"{requested_periods}"
            )
    elif requested_periods:
        distinct_period = requested_periods
    elif data_asset == "actuals":
        distinct_period = get_previous_fiscal_year_period(jobDAO)
        logger.info(
            f"No year_period_list provided for '{data_asset}'; derived P-1 period: "
            f"{distinct_period}"
        )
    else:
        distinct_period = asset["period_selector"](df)
        logger.info(
            f"No year_period_list provided for '{data_asset}'; derived periods: "
            f"{distinct_period}"
        )

    logger.info(
        f"Manual IMO Fin upload of '{data_asset}' (input df: {config.INPUT_DF}, "
        f"file id: {config.FILE_ID}) for periods: {distinct_period}"
    )

    asset["uploader"](
        df,
        config.WORKSPACE_ID,
        config.MODEL_ID,
        config.FILE_ID,
        config.PROCESS_ID,
        distinct_period,
        jobDAO,
    )
