"""DDL for the actuals table."""


def actuals_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        actuals, resolving the write path from
        output_config.

    parameters:
        output_config:
            datatype: dict
            description: Output configuration containing table_name, data_base,
                write_path and write_format.
    return:
        datatype: dict
        description: Dictionary with keys primary_keys (["Code",
            "Fiscal_Year_Period"]) and ddl_statements (the rendered CREATE
            EXTERNAL TABLE statement).
    """
    full_table_name = output_config.get("table_name")

    catalog = full_table_name.split(".")[0]
    schema = full_table_name.split(".")[1]
    table = full_table_name.split(".")[2]

    if full_table_name == f"{catalog}.{schema}.{table}":
        output_config = dict(output_config)  # avoid mutating the original if reused elsewhere
        partition_cols = output_config.get("partition") or []
        output_config["partition_clause"] = (
            f"PARTITIONED BY ({', '.join(partition_cols)})" if partition_cols else ""
        )
        ddl_statements = """
            CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                Code STRING,
                Fiscal_Year_Period STRING,
                Submission_Type_ID INT,
                Submission_Type STRING,
                Unit_ID STRING,
                Unit_Description STRING,
                Reporting_Line_ID STRING,
                Reporting_Line_Description STRING,
                Common_Item_ID STRING,
                Common_Item STRING,
                Representative_Material_ID STRING,
                Representative_Material STRING,
                Customer_ID STRING,
                Customer_Description STRING,
                Destination_ID STRING,
                Destination_Description STRING,
                Customer_Destination_ID STRING,
                Value DOUBLE
            )
            USING {write_format}
            {partition_clause}
            LOCATION '{write_path}'
            TBLPROPERTIES (
                'region' = 'NA',
                'lineage' = '',
                'segment' = 'MARS MW',
                'source_system' = 'finsight'
            )
        """.format(
            **output_config
        )
        primary_keys = ["Code", "Fiscal_Year_Period"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
