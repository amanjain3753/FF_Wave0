from simpel.interface.dao import IJobDAO

from mwd30anaplan.data_engineering.data_processing.constants import (
    ANAPLAN_API_PROCESS,
)
from mwd30anaplan.data_engineering.data_processing.feature.common_functions import (
    get_forward_fiscal_year_periods,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_imo_anaplan import (
    imo_fin_run_anaplan_process,
    imo_fin_run_anaplan_process_actuals,
)
from mwd30anaplan.data_engineering.data_processing.feature.feature_trigger_date_check_imo import (
    get_anchor_period_info,
    previous_year_period,
)


def imo_fin_anaplan_api_process(jobDAO: IJobDAO, process_date: str):
    """
    Run the Anaplan API upload processes for IMO Fin data (everything except
    Actuals, which is handled by ``imo_fin_actuals_api_process``).

    Each dataset is read from ``jobDAO.data_dict`` and pushed to its own
    Anaplan workspace/model/file via ``imo_fin_run_anaplan_process``, which
    uploads the file, triggers the linked import process and waits for the
    task to finish before the next dataset starts.


    Args:
        jobDAO       : Job DAO providing ``data_dict``, ``args`` and ``logger``.
        process_date : Pipeline run date supplied by the scheduler. Not used
                       here - the datasets are already filtered upstream - but
                       kept to match the DAG task signature.

    Raises:
        SystemExit: Propagated from the feature layer when an upload or an
            Anaplan import task fails; the remaining datasets are not uploaded.
    """
    df_dict = jobDAO.data_dict

    tpm_df = df_dict[ANAPLAN_API_PROCESS.TPM.INPUT_DF]
    imo_fin_run_anaplan_process(
        tpm_df,
        ANAPLAN_API_PROCESS.TPM.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.TPM.MODEL_ID,
        ANAPLAN_API_PROCESS.TPM.FILE_ID,
        ANAPLAN_API_PROCESS.TPM.PROCESS_ID,
        get_forward_fiscal_year_periods(tpm_df, jobDAO, process_name="TPM"),
        jobDAO,
    )

    supply_df = df_dict[ANAPLAN_API_PROCESS.SUPPLY.INPUT_DF]
    imo_fin_run_anaplan_process(
        supply_df,
        ANAPLAN_API_PROCESS.SUPPLY.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.SUPPLY.MODEL_ID,
        ANAPLAN_API_PROCESS.SUPPLY.FILE_ID,
        ANAPLAN_API_PROCESS.SUPPLY.PROCESS_ID,
        get_forward_fiscal_year_periods(supply_df, jobDAO, process_name="SUPPLY"),
        jobDAO,
    )

    demand_df = df_dict[ANAPLAN_API_PROCESS.DEMAND.INPUT_DF]
    imo_fin_run_anaplan_process(
        demand_df,
        ANAPLAN_API_PROCESS.DEMAND.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.DEMAND.MODEL_ID,
        ANAPLAN_API_PROCESS.DEMAND.FILE_ID,
        ANAPLAN_API_PROCESS.DEMAND.PROCESS_ID,
        get_forward_fiscal_year_periods(demand_df, jobDAO, process_name="DEMAND"),
        jobDAO,
    )

    # imo_fin_run_anaplan_process(
    #     df_dict[ANAPLAN_API_PROCESS.PRODUCT_MASTERDATA.INPUT_DF],
    #     ANAPLAN_API_PROCESS.PRODUCT_MASTERDATA.WORKSPACE_ID,
    #     ANAPLAN_API_PROCESS.PRODUCT_MASTERDATA.MODEL_ID,
    #     ANAPLAN_API_PROCESS.PRODUCT_MASTERDATA.FILE_ID,
    #     ANAPLAN_API_PROCESS.PRODUCT_MASTERDATA.PROCESS_ID,
    #     None,
    #     jobDAO,
    #     process_name="PRODUCT_MASTERDATA",
    # )

    imo_fin_run_anaplan_process(
        df_dict[ANAPLAN_API_PROCESS.CUSTOMER_PRICE_LIST.INPUT_DF],
        ANAPLAN_API_PROCESS.CUSTOMER_PRICE_LIST.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.CUSTOMER_PRICE_LIST.MODEL_ID,
        ANAPLAN_API_PROCESS.CUSTOMER_PRICE_LIST.FILE_ID,
        ANAPLAN_API_PROCESS.CUSTOMER_PRICE_LIST.PROCESS_ID,
        None,
        jobDAO,
        process_name="CUSTOMER_PRICE_LIST",
    )

    imo_fin_run_anaplan_process(
        df_dict[ANAPLAN_API_PROCESS.STANDARD_COST.INPUT_DF],
        ANAPLAN_API_PROCESS.STANDARD_COST.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.STANDARD_COST.MODEL_ID,
        ANAPLAN_API_PROCESS.STANDARD_COST.FILE_ID,
        ANAPLAN_API_PROCESS.STANDARD_COST.PROCESS_ID,
        None,
        jobDAO,
        process_name="STANDARD_COST",
    )

    imo_fin_run_anaplan_process(
        df_dict[ANAPLAN_API_PROCESS.ICP.INPUT_DF],
        ANAPLAN_API_PROCESS.ICP.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.ICP.MODEL_ID,
        ANAPLAN_API_PROCESS.ICP.FILE_ID,
        ANAPLAN_API_PROCESS.ICP.PROCESS_ID,
        None,
        jobDAO,
        process_name="ICP",
    )


def imo_fin_actuals_api_process(jobDAO: IJobDAO, process_date: str):
    """
    Run the Anaplan API upload process for IMO Fin Actuals.

    Actuals is kept separate from the other datasets because of its volume: it
    is routed through ``imo_fin_run_anaplan_process_actuals``, which clears the
    previous run's staging area, then for every fiscal period decides between a
    single-shot upload and a chunked upload (compressed CSV chunks staged on
    ADLS and pushed one at a time, running the Anaplan import process after
    each chunk).

    Only the previous fiscal period (P-1) is uploaded, matching what
    ``ACTUALS_PROCESS`` wrote earlier in the same run. The period is resolved the
    same way the trigger date check resolves it: ``process_date`` is looked up in
    the Mars calendar to get the current period, and ``previous_year_period``
    steps one period back. It is not derived from the DataFrame - the actuals
    table is written with dynamic partition overwrite and therefore still holds
    every period ever processed.

    ``previous_year_period`` returns a numeric period (``202608``) while the
    actuals DataFrame stores ``Fiscal_Year_Period`` as a string (``'P8 FY26'``),
    so the value is converted before it reaches the feature layer.

    Args:
        jobDAO       : Job DAO providing ``data_dict``, ``args`` and ``logger``.
        process_date : Pipeline run date supplied by the scheduler. Not used
                       directly - the run date is read from
                       ``env_config_dict['process_date_value']`` so the format
                       matches the Mars calendar - but kept to match the DAG
                       task signature.

    Raises:
        ValueError: When the run date is missing from the environment config, or
            when it cannot be resolved against the Mars calendar (propagated from
            ``get_anchor_period_info``).
        SystemExit: Propagated from the feature layer when a chunk upload or an
            Anaplan import task fails.
    """
    logger = jobDAO.logger
    df_dict = jobDAO.data_dict

    actuals_df = df_dict[ANAPLAN_API_PROCESS.ACTUALS_NEW.INPUT_DF]
    df_mars_calander = df_dict["mars_cal"]

    # Same normalisation the trigger date check does: the framework hands over
    # "20260831" but the Mars calendar Date column is "2026-08-31".
    process_date_raw = jobDAO.env_config_dict.get("process_date_value") or ""
    process_date_raw = str(process_date_raw)
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
        f"Actuals upload period: run_date={run_date}, "
        f"current={current_year_period}, P-1={upload_year_period} -> {distinct_period}"
    )
    imo_fin_run_anaplan_process_actuals(
        actuals_df,
        ANAPLAN_API_PROCESS.ACTUALS_NEW.WORKSPACE_ID,
        ANAPLAN_API_PROCESS.ACTUALS_NEW.MODEL_ID,
        ANAPLAN_API_PROCESS.ACTUALS_NEW.FILE_ID,
        ANAPLAN_API_PROCESS.ACTUALS_NEW.PROCESS_ID,
        distinct_period,
        jobDAO,
    )
 