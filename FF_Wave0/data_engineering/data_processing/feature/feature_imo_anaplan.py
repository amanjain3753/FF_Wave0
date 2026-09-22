import io
import json
import math
import time
from datetime import datetime, timedelta
from simpel.interface.dao import IJobDAO
import requests
import gzip
from pyspark.sql import Row, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)
from simpel.utils.db_utils import get_dbutils


from mwd30anaplan.data_engineering.data_processing.constants import ANAPLAN_API_PROCESS

spark = SparkSession.builder.getOrCreate()
dbutils = get_dbutils(spark)
UPLOAD_SIZE_THRESHOLD_GB = 3
UPLOAD_STAGING_ROOT = (
    "abfss://output@dnafinlakeeus2devsa.dfs.core.windows.net/"
    "MWD30ANAPLAN/upload_staging"
)


client_id = dbutils.secrets.get(
    scope="MWD30ANAPLAN-SECRETSCOPE", key="clientid-anaplan"
)
refresh_token = dbutils.secrets.get(
    scope="MWD30ANAPLAN-SECRETSCOPE", key="refresh-token-anaplan"
)


# -----------------------------add here for actuals-------------------------------------
def imo_fin_run_anaplan_process(
    df, workspace_id, model_id, file_id, process_id, distinct_period, jobDAO: IJobDAO,process_name="UNKNOWN"
):
    """
    Orchestrates the Anaplan end-to-end workflow:
      1. Uploads the given DataFrame to the specified Anaplan file.
      2. Triggers the Anaplan import/process associated with the file.
      3. Monitors the task execution status until completion.
      4. Returns the final task result/metadata.

    Args:
        df : DataFrame to upload to Anaplan.
        workspace_id: Anaplan workspace identifier.
        model_id: Anaplan model identifier.
        file_id: Anaplan file identifier.
        process_id: Anaplan process identifier.
        distinct_period: List of unique Period values for which data will be uploaded.

    """
    logger = jobDAO.logger
    logger.info(f"[{process_name}] imo_fin_run_anaplan_process started")
    
    access_token = get_access_token_using_refresh_token(
        client_id, refresh_token, jobDAO
    )
    last_refresh = datetime.now()
    logger.info(f"Token refreshed at {last_refresh}")
    url = (
        f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/files"
    )
    headers = {
        "Authorization": f"AnaplanAuthToken {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        file_name = None
        for f in data.get("files", []):
            if f["id"] == file_id:
                file_name = f["name"]
                logger.info(f"File Details: {f}")
                break
        if not file_name:
            logger.error(f"File ID {file_id} not found in Anaplan response.")
            return {"status": "Failed", "message": "File ID not found"}
    else:
        logger.error(f"Error fetching files: {response.status_code}, {response.text}")
        return {"status": "Failed", "message": response.text}
    if distinct_period:
        logger.info(
            f"Periods queued for data load: {distinct_period}"
        )

        for i in distinct_period:
            logger.info(f"Filter Data for period: {i}")

            df_filtered = df.filter(df["Fiscal_Year_Period"] == i)
            logger.info(f"data filtered for {i}")
            if datetime.now() - last_refresh > timedelta(minutes=25):
                access_token = get_access_token_using_refresh_token(
                    client_id, refresh_token, jobDAO
                )
                last_refresh = datetime.now()
                logger.info(f"Token refreshed at {last_refresh}")

            logger.info(f"before upload function---{i}")
            logger.info(
                f"UPLOADING FILE TO Anaplan API: {i}(FISCAL_YEAR_PERIOD)..."
            )
            resp = upload_files_to_api(
                df_filtered,
                access_token,
                workspace_id,
                model_id,
                file_id,
                file_name,
                jobDAO,
                i,
            )
            if resp == 204:
                logger.info("File uploaded successfully.")
                logger.info("Running process...")
                task_id = run_process(
                    access_token, workspace_id, model_id, process_id, jobDAO
                )
            else:
                raise SystemExit(
                    f"API call failed: {response['status_code']} - {response['text']}"
                )

            logger.info(
                f"Checking task status for ID: {task_id}..."
            )
            task_info = get_task_info(
                access_token,
                workspace_id,
                model_id,
                file_id,
                file_name,
                process_id,
                task_id,
                i,
                jobDAO,
            )
            logger.info(f"TASK INFO:{task_info}")
    else:
        logger.info(f"2---")
        logger.info(f"UPLOADING {file_name} TO Anaplan API...")
        resp = upload_files_to_api(
            df, access_token, workspace_id, model_id, file_id, file_name, jobDAO, None
    )
        if resp == 204:
            logger.info("File uploaded successfully.")
            logger.info("Running process...")
            task_id = run_process(access_token, workspace_id, model_id, process_id, jobDAO)
        else:
            raise SystemExit(
            f"API call failed: {response['status_code']} - {response['text']}"
        )

        logger.info(f"Checking task status for ID: {task_id}...")
        task_info = get_task_info(
        access_token,
        workspace_id,
        model_id,
        file_id,
        file_name,
        process_id,
        task_id,
        None,
        jobDAO,
    )
        logger.info(f"TASK INFO:{task_info}")


def _clear_upload_staging(staging_root, logger):
    """
    Delete the chunk files left behind by the *previous* pipeline run.

    Staged chunks are deliberately kept on ADLS after a run finishes so they
    stay available for inspection / re-upload. They are only removed here, once,
    at the start of the next run - never at the end of the current one and never
    between fiscal periods within the same run.
    """
    try:
        dbutils.fs.rm(staging_root, recurse=True)
        logger.info(f"Cleared staging path from previous run: {staging_root}")
    except Exception:
        logger.info(f"Nothing to clear at staging path: {staging_root}")


def imo_fin_run_anaplan_process_actuals(
    df, workspace_id, model_id, file_id, process_id, distinct_period, jobDAO: IJobDAO
):
    """
    Orchestrates the Anaplan end-to-end workflow:
      1. Uploads the given DataFrame to the specified Anaplan file.
      2. Triggers the Anaplan import/process associated with the file.
      3. Monitors the task execution status until completion.
      4. Returns the final task result/metadata.

    Args:
        df : DataFrame to upload to Anaplan.
        workspace_id: Anaplan workspace identifier.
        model_id: Anaplan model identifier.
        file_id: Anaplan file identifier.
        process_id: Anaplan process identifier.
        distinct_period: List of unique Period values for which data will be uploaded.

    """
    

    logger = jobDAO.logger
    access_token = get_access_token_using_refresh_token(
        client_id, refresh_token, jobDAO
    )
    logger.info(f"after token refresh")
    last_refresh = datetime.now()
    logger.info(f"Token refreshed at {last_refresh}")
    url = (
        f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/files"
    )
    headers = {
        "Authorization": f"AnaplanAuthToken {access_token}",
        "Content-Type": "application/json",
    }
    # response = requests.get(url, headers=headers)
    response = requests.get(
        url,
        headers=headers,
        timeout=120,
    )

    if response.status_code == 200:
        data = response.json()
        file_name = None
        for f in data.get("files", []):
            if f["id"] == file_id:
                file_name = f["name"]
                logger.info(f"File Details: {f}")
                break
        if not file_name:
             logger.error(f"File ID {file_id} not found in Anaplan response.")
             return {"status": "Failed", "message": "File ID not found"}
    else:
         logger.error(f"Error fetching files: {response.status_code}, {response.text}")
         return {"status": "Failed", "message": response.text}

    # Wipe the previous run's chunks once, here, before any period is uploaded.
    # Every period below then writes into its own timestamped sub-folder and
    # nothing is deleted again until the next pipeline run reaches this line.
    _clear_upload_staging(UPLOAD_STAGING_ROOT, logger)

    if distinct_period:
        logger.info(
            f"Periods queued for data load: {distinct_period}"
        )
        

        for i in distinct_period:
            logger.info(f"Filter Data for period: {i}")

            df_filtered = df.filter(df["Fiscal_Year_Period"] == i)
            # df_filtered = df_filtered.drop("Fiscal_Year_Period")
            if datetime.now() - last_refresh > timedelta(minutes=25):
                access_token = get_access_token_using_refresh_token(
                    client_id, refresh_token, jobDAO
                )
                last_refresh = datetime.now()
                logger.info(f"Token refreshed at {last_refresh}")

            logger.info(f"3---")
            logger.info(
                f"UPLOADING FILE TO Anaplan API: {i}(FISCAL_YEAR_PERIOD)..."
            )
            resp = upload_dispatcher(
                df_filtered,
                access_token,
                workspace_id,
                model_id,
                file_id,
                file_name,
                jobDAO,
                i,
                process_id=process_id,
            )
            if resp != 204:
                raise SystemExit(
                    f"Upload failed for period {i}: did not return 204"
                )
            logger.info(
                f"Period {i} - All chunks uploaded and processed successfully."
            )
    else:
        logger.info(f"4---")
        logger.info(f"UPLOADING {file_name} TO Anaplan API via dispatcher...")
        resp = upload_dispatcher(
            df,
            access_token,
            workspace_id,
            model_id,
            file_id,
            file_name,
            jobDAO,
            None,
            process_id=process_id,
        )
        if resp != 204:
            raise SystemExit(
                f"Upload failed: did not return 204"
            )
        logger.info("Full load - All chunks uploaded and processed successfully.")



def get_access_token_using_refresh_token(client_id, refresh_token, jobDAO: IJobDAO):
    """
    Generate a new access token from Anaplan using a refresh token.

    Parameters
    ----------
    client_id : Anaplan client ID.
    refresh_token :Refresh token previously issued.

    Returns
    -------
    New access token if successful.

    """

    logger = jobDAO.logger
    url = "https://us1a.app.anaplan.com/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        resp_json = response.json()
        token = resp_json.get("access_token")
        logger.info("New Access token generated")
        return token
    else:
        raise SystemExit(
            f"API call failed: {response['status_code']} - {response['text']}"
        )



def update_logs(
    workspace_id,
    model_id,
    file_name,
    file_id,
    process_id,
    fiscal_year_period,
    jobDAO: IJobDAO,
    file_size=None,
    total_rows=None,
    status=None,
    action=None,
    timestamp=None,
    message=None,
):
    """
    Write an execution log entry into the Delta table API_LOGS.

    Creates the table if it doesn’t exist and appends details of
    Anaplan file uploads or process runs (IDs, status, size, rows,
    timestamp, and API response).

    Parameters
    ----------
    workspace_id : str
    model_id : str
    file_name : str
    file_id : str or int
    process_id : str or int
    fiscal_year_period : str
    file_size : floatupload_dispatcher
    total_rows : int
    status : str
    action : str
    timestamp : datetime
    message : str
    """
    logger = jobDAO.logger

    env_var = jobDAO.args.get("environment")
    env_var = env_var.lower()
    table_name = ANAPLAN_API_PROCESS.LOGS.format(ENV=env_var)
    logger.info(f"LOG TABLE NAME: {table_name}")

    # Schema
    schema = StructType(
        [
            StructField("Workspace_ID", StringType(), True),
            StructField("Model_ID", StringType(), True),
            StructField("File_ID", StringType(), True),
            StructField("File_Name", StringType(), True),
            StructField("Process_ID", StringType(), True),
            StructField("Fiscal_Year_Period", StringType(), True),
            StructField("File_Size_MB", DoubleType(), True),
            StructField("Total_Rows", IntegerType(), True),
            StructField("Status", StringType(), True),
            StructField("Action", StringType(), True),
            StructField("Created_Timestamp", TimestampType(), True),
            StructField("JSON_Response", StringType(), True),
        ]
    )

    # Ensure table exists
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            Workspace_ID STRING,
            Model_ID STRING,
            File_ID STRING,
            File_Name STRING,
            Process_ID STRING,
            Fiscal_Year_Period STRING,
            -- Chunk INT,
            File_Size_MB DOUBLE,
            Total_Rows INT,
            Status STRING,
            Action STRING,
            Created_Timestamp TIMESTAMP,
            JSON_Response STRING
        )
        USING DELTA
    """
    )

    row = Row(
        Workspace_ID=workspace_id,
        Model_ID=model_id,
        File_ID=str(file_id) if file_id else None,
        File_Name=file_name,
        Process_ID=str(process_id) if process_id else None,
        Fiscal_Year_Period=fiscal_year_period,
        File_Size_MB=float(file_size) if file_size is not None else None,
        Total_Rows=int(total_rows) if total_rows is not None else None,
        Status=status,
        Action=action,
        Created_Timestamp=timestamp,
        JSON_Response=(
            json.dumps(message) if isinstance(message, (dict, list)) else str(message)
        ),
    )

    log_df = spark.createDataFrame([row], schema=schema)

    try:
        spark.read.table(table_name)
        log_df.write.format("delta").mode("append").saveAsTable(table_name)
    except Exception:
        log_df.write.format("delta").mode("overwrite").saveAsTable(table_name)


# ------------------------------------add here for actuals------------------------



def upload_files_to_api(
    df,
    access_token,
    workspace_id,
    model_id,
    file_id,
    file_name,
    jobDAO: IJobDAO,
    fiscal_year_period,
    retry=True,
):
    logger = jobDAO.logger
    # ---- Convert Spark DF -> Pandas -> CSV ----
    csv_buffer = io.StringIO()
    df.toPandas().to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    # ---- Gzip compress ----
    gzip_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as gz:
        gz.write(csv_bytes)

    gzip_bytes = gzip_buffer.getvalue()
    size_mb = round(len(csv_bytes) / (1024 * 1024), 2)  # size of file
    row_count = df.count()  # row count of file
    logger.info(f"The Count of row is {row_count}")
    headers = {
        "Authorization": f"AnaplanAuthToken {access_token}",
        "Content-Type": "application/x-gzip",
    }

    logger.info(
        f"Original CSV size (MB): {round(len(csv_bytes) / (1024*1024), 2)}"
    )
    logger.info(
        f"Compressed size (MB): {round(len(gzip_bytes) / (1024*1024), 2)}"
    )

    # ---- Upload to Anaplan ----
    upload_url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/files/{file_id}"
    

    resp = requests.put(upload_url, headers=headers, data=gzip_bytes)

    logger.info(
        f"Upload Response: {resp.status_code} {resp.text}"
    )
    if resp.status_code != 204 and retry:
        update_logs(
            workspace_id=workspace_id,
            model_id=model_id,
            file_id=None,
            file_name=None,
            process_id=None,
            file_size=None,
            fiscal_year_period=fiscal_year_period,
            jobDAO=jobDAO,
            total_rows=None,
            status="Success" if resp.status_code == 204 else "Failed",
            action="File Upload",
            timestamp=datetime.now(),
            message=resp.text,
        )
        access_token = get_access_token_using_refresh_token(
            client_id, refresh_token, jobDAO
        )
        return upload_files_to_api(
            df,
            access_token,
            workspace_id,
            model_id,
            file_id,
            file_name,
            jobDAO,
            fiscal_year_period,
            retry=False,
        )
    elif resp.status_code == 204:
        update_logs(
            workspace_id=workspace_id,
            model_id=model_id,
            file_id=file_id,
            file_name=file_name,
            process_id=None,
            file_size=size_mb,
            fiscal_year_period=fiscal_year_period,
            jobDAO=jobDAO,
            total_rows=row_count,
            status="Succeeded" if resp.status_code == 204 else "Failed",
            action="File Upload",
            timestamp=datetime.now(),
            message=resp.text,
        )
        return 204
    else:
        raise SystemExit(f"API call failed: {resp['status_code']} - {resp['text']}")



def upload_dispatcher(
    df,
    access_token,
    workspace_id,
    model_id,
    file_id,
    file_name,
    jobDAO: IJobDAO,
    fiscal_year_period,
    process_id=None,
    staging_root=UPLOAD_STAGING_ROOT,
    retry=True,
):
    """
    Decides whether to use the chunked upload (upload_files_to_api_actuals) or the
    single-shot upload (upload_files_to_api), based on estimated DataFrame size.

    ``process_id`` is only forwarded to the chunked path, where it triggers the
    per-chunk run-process/wait cycle.  The single-shot path never runs the
    process; that stays the caller's responsibility.
    """
    logger = jobDAO.logger
    logger.info(
        "Estimating DataFrame size to decide upload strategy..."
    )

    df = df.cache()

    estimated_bytes = _estimate_df_size_bytes(df)
    estimated_gb = estimated_bytes / (1024**3)
    logger.info(f"Estimated size: {estimated_gb:.2f} GB")

    if estimated_gb > UPLOAD_SIZE_THRESHOLD_GB:
        logger.info(
            f"Size {estimated_gb:.2f} GB > {UPLOAD_SIZE_THRESHOLD_GB} GB threshold "
            "-> using chunked upload (upload_files_to_api_actuals)"
        )
        return upload_files_to_api_actuals(
            df,
            access_token,
            workspace_id,
            model_id,
            file_id,
            file_name,
            jobDAO,
            fiscal_year_period,
            process_id=process_id,
            staging_root=staging_root,
            retry=retry,
            estimated_bytes=estimated_bytes,
        )
    else:
        logger.info(
            f"Size {estimated_gb:.2f} GB <= {UPLOAD_SIZE_THRESHOLD_GB} GB threshold "
            "-> using single-shot upload (upload_files_to_api)"
        )
        resp = upload_files_to_api(
            df,
            access_token,
            workspace_id,
            model_id,
            file_id,
            file_name,
            jobDAO,
            fiscal_year_period,
            retry=retry,
        )
        # The chunked path runs the import process per chunk; the single-shot
        # path has to run it once here so both branches return with the data
        # already imported.
        if resp == 204 and process_id is not None:
            logger.info("Running Anaplan import process for single-shot upload...")
            task_id = run_process(
                access_token, workspace_id, model_id, process_id, jobDAO
            )
            logger.info(f"Process started. Task ID: {task_id}")
            task_info = get_task_info(
                access_token=access_token,
                workspace_id=workspace_id,
                model_id=model_id,
                file_id=file_id,
                file_name=file_name,
                process_id=process_id,
                task_id=task_id,
                fiscal_year_period=fiscal_year_period,
                jobDAO=jobDAO,
            )
            logger.info(f"TASK INFO:{task_info}")
        return resp


def _estimate_df_size_bytes(df):
    """
    Estimate the uncompressed CSV size of a Spark DataFrame in bytes
    without collecting data to the driver.

    Strategy
    --------
    Sample 1 % of rows (min 1 000, max 10 000), serialise the sample to
    CSV in memory, then extrapolate to the full row count.  This avoids a
    full ``toPandas()`` scan while remaining accurate enough for chunk
    sizing (±10–20 % is fine; we are rounding up to whole chunks anyway).

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        The DataFrame that will be uploaded.

    Returns
    -------
    int
        Estimated total CSV size in bytes.
    """
    total_rows = df.count()
    if total_rows == 0:
        return 0

    sample_size = max(1_000, min(10_000, int(total_rows * 0.01)))
    sample_df = df.limit(sample_size)

    buf = io.StringIO()
    sample_df.toPandas().to_csv(buf, index=False, encoding="utf-8")
    sample_bytes = len(buf.getvalue().encode("utf-8"))

    estimated_bytes = int(sample_bytes * (total_rows / sample_size))
    return estimated_bytes



def upload_files_to_api_actuals(
    df,
    access_token,
    workspace_id,
    model_id,
    file_id,
    file_name,
    jobDAO: IJobDAO,
    fiscal_year_period,
    process_id=None,
    staging_root=UPLOAD_STAGING_ROOT,
    retry=True,
    estimated_bytes=None,
):
    logger = jobDAO.logger
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    TARGET_CHUNK_GB = 2.0
    CSV_MULTIPLIER  = 2.0

    # ------------------------------------------------------------------
    # 1. Estimate size to decide: single-shot or chunked upload
    # ------------------------------------------------------------------
    logger.info("Estimating DataFrame size...")
    if estimated_bytes is None:
        estimated_bytes = _estimate_df_size_bytes(df)
    estimated_csv_gb = (estimated_bytes / (1024 ** 3)) * CSV_MULTIPLIER
    logger.info(f"Estimated CSV size: {estimated_csv_gb:.2f} GB")

    upload_url = (
        f"https://api.anaplan.com/2/0/workspaces/{workspace_id}"
        f"/models/{model_id}/files/{file_id}"
    )

    # ==================================================================
    # Chunked upload
    # ==================================================================
    num_chunks = max(1, math.ceil(estimated_csv_gb / TARGET_CHUNK_GB))
    logger.info(f"Using CHUNKED upload → {num_chunks} chunk(s)")

    total_rows = df.count()
    logger.info(f"Total rows to upload: {total_rows}")

    # ------------------------------------------------------------------
    # Write partitioned Parquet to ADLS staging (chunk_id = 0..N-1)
    # ------------------------------------------------------------------
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_path = f"{staging_root}/{ts}"

    logger.info(f"Writing backup to ADLS staging (Parquet): {output_path}")
    original_cols = df.columns
    df.write.mode("overwrite").parquet(output_path)
    df = spark.read.parquet(output_path).select(*original_cols)

    cols = df.columns
    last_refresh = datetime.now()
    total_start = time.time()

    for i in range(num_chunks):
        chunk_num = i + 1

        # Proactively refresh token every 25 minutes
        if datetime.now() - last_refresh > timedelta(minutes=25):
            access_token = get_access_token_using_refresh_token(client_id, refresh_token, jobDAO)
            last_refresh = datetime.now()
            logger.info(f"Token refreshed at {last_refresh}")

        logger.info(f"{'='*60}")
        logger.info(f"Processing chunk {chunk_num}/{num_chunks}")
        logger.info(f"{'='*60}")

        # --- Filter chunk from SOURCE df using hash (keeps MANY partitions) ---
        # This works like PATH A: toPandas() distributes across all executors
        chunk_df = df.filter(F.abs(F.hash(F.struct(*cols))) % num_chunks == i).repartition(25)

        chunk_start = time.time()
        csv_buffer = io.StringIO()
        chunk_df.toPandas().to_csv(csv_buffer, index=False, encoding="utf-8")
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        gzip_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as gz:
            gz.write(csv_bytes)
        gzip_bytes = gzip_buffer.getvalue()

        size_mb = round(len(gzip_bytes) / (1024 * 1024), 2)
        csv_size_mb = round(len(csv_bytes) / (1024 * 1024), 2)
        logger.info(f"Chunk {chunk_num} CSV size: {csv_size_mb} MB | Compressed: {size_mb} MB")
        del csv_buffer, csv_bytes
        elapsed = round(time.time() - chunk_start, 2)
        logger.info(f"Chunk {chunk_num}/{num_chunks} — toPandas + CSV + gzip took {elapsed}s")


        headers = {
            "Authorization": f"AnaplanAuthToken {access_token}",
            "Content-Type": "application/x-gzip",
        }

        resp = requests.put(upload_url, headers=headers, data=gzip_bytes)
        logger.info(f"Chunk {chunk_num} upload response: {resp.status_code} {resp.text}")

        # Free gzip bytes after upload
        del gzip_buffer, gzip_bytes

        if resp.status_code != 204:
            update_logs(
                workspace_id=workspace_id, model_id=model_id,
                file_id=file_id, file_name=file_name, process_id=process_id,
                file_size=size_mb, fiscal_year_period=fiscal_year_period,
                jobDAO=jobDAO,
                total_rows=None,
                status="Failed", action=f"File Upload (chunk {chunk_num}/{num_chunks})",
                timestamp=datetime.now(), message=resp.text,
            )
            if retry:
                logger.warning(
                    f"Chunk {chunk_num} upload failed ({resp.status_code}). "
                    "Refreshing token and retrying once..."
                )
                access_token = get_access_token_using_refresh_token(
                    client_id, refresh_token, jobDAO
                )
                # Re-read chunk for retry (hash filter from source df)
                chunk_df_retry = df.filter(F.abs(F.hash(F.struct(*cols))) % num_chunks == i).repartition(25)
                csv_buffer = io.StringIO()
                chunk_df_retry.toPandas().to_csv(csv_buffer, index=False, encoding="utf-8")
                csv_bytes = csv_buffer.getvalue().encode("utf-8")
                gzip_buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as gz:
                    gz.write(csv_bytes)
                gzip_bytes = gzip_buffer.getvalue()
                del csv_buffer, csv_bytes

                retry_resp = requests.put(
                    upload_url,
                    headers={
                        "Authorization": f"AnaplanAuthToken {access_token}",
                        "Content-Type": "application/x-gzip",
                    },
                    data=gzip_bytes,
                )
                del gzip_buffer, gzip_bytes
                logger.info(f"Retry chunk {chunk_num} response: {retry_resp.status_code} {retry_resp.text}")
                if retry_resp.status_code != 204:
                    raise SystemExit(
                        f"Chunk {chunk_num} upload failed after retry: "
                        f"{retry_resp.status_code} - {retry_resp.text}"
                    )
            else:
                raise SystemExit(
                    f"Chunk {chunk_num} upload failed: {resp.status_code} - {resp.text}"
                )

        update_logs(
            workspace_id=workspace_id, model_id=model_id,
            file_id=file_id, file_name=file_name, process_id=process_id,
            file_size=size_mb, fiscal_year_period=fiscal_year_period,
            jobDAO=jobDAO,
            total_rows=total_rows if chunk_num == num_chunks else None,
            status="Succeeded", action=f"File Upload (chunk {chunk_num}/{num_chunks})",
            timestamp=datetime.now(), message=resp.text,
        )
        logger.info(f"Chunk {chunk_num}/{num_chunks} uploaded successfully.")

        # --- Run Anaplan import process after this chunk ---
        if process_id is None:
            logger.info(
                f"No process_id supplied - skipping import process for "
                f"chunk {chunk_num}/{num_chunks}."
            )
            continue
            
        logger.info(f"Starting Anaplan import process for chunk {chunk_num}/{num_chunks}...")
        task_id = run_process(access_token, workspace_id, model_id, process_id, jobDAO)
        logger.info(f"Process started. Task ID: {task_id}")

        task_info = get_task_info(
            access_token=access_token,
            workspace_id=workspace_id,
            model_id=model_id,
            file_id=file_id,
            file_name=file_name,
            process_id=process_id,
            task_id=task_id,
            fiscal_year_period=fiscal_year_period,
            jobDAO=jobDAO,
        )
        logger.info(
            f"Chunk {chunk_num}/{num_chunks} - Upload + Import Process "
            f"completed successfully. File: {file_name}"
        )

    total_elapsed = round(time.time() - total_start, 2)
    logger.info(f"All chunks complete — {num_chunks} chunks, total conversion time: {total_elapsed}s")
    return 204

def run_process(access_token, workspace_id, model_id, process_id, jobDAO: IJobDAO):
    """
    Run an Anaplan process by starting a task.

    Parameters
    ----------
    access_token : str
        Valid Anaplan access token.
    workspace_id : str
        Anaplan workspace ID.
    model_id : str
        Anaplan model ID.
    process_id : str
        Anaplan process ID.

    Returns
    -------
    str
        Task ID of the triggered process.
    """
    url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/processes/{process_id}/tasks"
    logger = jobDAO.logger
    headers = {
        "Authorization": f"AnaplanAuthToken {access_token}",
        "Content-Type": "application/json",
    }

    payload = {"localeName": "en_US"}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 401:
        access_token = get_access_token_using_refresh_token(
            client_id, refresh_token, jobDAO
        )
        logger.info("Retrying after refreshing the token")
        return run_process(access_token, workspace_id, model_id, process_id, jobDAO)
    elif response.status_code == 200:
        task_id = response.json()["task"]["taskId"]
        logger.info("Process Ran Successfully...")
        return task_id
    else:
        raise Exception(f"Error starting process: {response.text}")



def get_task_info(
    access_token,
    workspace_id,
    model_id,
    file_id,
    file_name,
    process_id,
    task_id,
    fiscal_year_period,
    jobDAO: IJobDAO,
    max_retries=120,
    wait_sec=60,
):
    """
    Polls Anaplan for task status until completion or max retries.

    Parameters
    ----------
    access_token : str
        Valid Anaplan access token.
    workspace_id : str
        Anaplan workspace ID.
    model_id : str
        Anaplan model ID.
    file_id : str or int
        File ID linked to the process.
    file_name : str
        File name for logging.
    process_id : str
        Anaplan process ID.
    task_id : str
        Task ID returned by `run_process`.
    fiscal_year_period : str
        Fiscal year-period tag for logging.
    max_retries : int, optional
        Number of polling attempts before giving up. Default = 5.
    wait_sec : int, optional
        Seconds to wait between retries. Default = 60.

    Returns
    -------
    dict
        Task information JSON from Anaplan API.

    """
    url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/processes/{process_id}/tasks/{task_id}/"
    logger = jobDAO.logger
    headers = {
        "Authorization": f"AnaplanAuthToken {access_token}",
        "Content-Type": "application/json",
    }

    retries = 0
    while retries < max_retries:
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            logger.warning("Access token expired. Refreshing token...")
            access_token = get_access_token_using_refresh_token(
                client_id, refresh_token, jobDAO
            )
            headers["Authorization"] = f"AnaplanAuthToken {access_token}"
            retries += 1
            continue

        elif response.status_code == 200:
            task_info = response.json()
            task_state = task_info.get("task", {}).get("taskState")
            if task_state == "IN_PROGRESS":
                logger.info(
                    f"Task is still running. Waiting {wait_sec} sec..."
                )
                time.sleep(wait_sec)
                retries += 1
                continue
            elif task_state == "COMPLETE":
                result = task_info["task"].get("result", {})
                top_failure = result.get("failureDumpAvailable", False)

                nested_failures = any(
                    nr.get("failureDumpAvailable", False)
                    for nr in result.get("nestedResults", [])
                )
                # ---process successs ---------------------
                process_success = result.get("successful", False)

                if process_success and not top_failure and not nested_failures:
                    logger.info(
                        "Task completed successfully. No failure dumps."
                    )
                    update_logs(
                        workspace_id=workspace_id,
                        model_id=model_id,
                        file_id=file_id,
                        file_name=file_name,
                        process_id=process_id,
                        file_size=None,
                        fiscal_year_period=fiscal_year_period,
                        jobDAO=jobDAO,
                        total_rows=0,
                        status="Succeeded",
                        action="Import Process",
                        timestamp=datetime.now(),
                        message=task_info,
                    )
                    return task_info

                # -------------------------------------------
                # SUCCESS WITH WARNINGS
                # -------------------------------------------
                elif process_success:
                    logger.warning(
                        "Task completed with warning/" "failure dumps available."
                    )

                    update_logs(
                        workspace_id=workspace_id,
                        model_id=model_id,
                        file_id=file_id,
                        file_name=file_name,
                        process_id=process_id,
                        file_size=None,
                        fiscal_year_period=fiscal_year_period,
                        jobDAO=jobDAO,
                        total_rows=None,
                        status="Succeeded with warnings",
                        action="Import Process",
                        timestamp=datetime.now(),
                        message=task_info,
                    )

                    return task_info

                else:
                    logger.error("Task completed but process failed.")

                    update_logs(
                        workspace_id=workspace_id,
                        model_id=model_id,
                        file_id=file_id,
                        file_name=file_name,
                        process_id=process_id,
                        file_size=None,
                        fiscal_year_period=fiscal_year_period,
                        jobDAO=jobDAO,
                        total_rows=None,
                        status="Failed",
                        action="Import Process",
                        timestamp=datetime.now(),
                        message=task_info,
                    )

                    raise SystemExit(
                        f"Task failed. " f"{response.status_code} - " f"{response.text}"
                    )

        # ---------------------------------------------------
        # OTHER API ERRORS

        else:
            logger.error(
                f"Failed to fetch task info: "
                f"{response.status_code} - "
                f"{response.text}"
            )

            update_logs(
                workspace_id=workspace_id,
                model_id=model_id,
                file_id=file_id,
                file_name=file_name,
                process_id=process_id,
                file_size=None,
                fiscal_year_period=fiscal_year_period,
                jobDAO=jobDAO,
                total_rows=None,
                status="Failed",
                action="Import Process",
                timestamp=datetime.now(),
                message=response.text,
            )

            response.raise_for_status()

    raise SystemExit(
        f"Task completed with failure dumps available. {response.status_code} - {response.text}"
    )
