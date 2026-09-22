"""DDL for the demand table."""


def demand_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        demand, resolving the write path from
        output_config.

    parameters:
        output_config:
            datatype: dict
            description: Output configuration containing table_name, data_base,
                write_path and write_format.
    return:
        datatype: dict
        description: Dictionary with keys primary_keys (["unique_key"]) and
            ddl_statements (the rendered CREATE EXTERNAL TABLE statement).
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
                unique_key STRING,
                Material_Number STRING,
                Material_Description STRING,
                Site STRING,
                Fiscal_year_period STRING,
                Customer_ID STRING,
                Customer_Description STRING,
                Demand_group STRING,
                Demand_group_description STRING,
                Forecast_Type_ID INT,
                Forecast_Type STRING,
                Building_Block_ID INT,
                Building_Block STRING,
                volume_cases DOUBLE,
                volume_tonnes DOUBLE,
                Sales_org STRING,
                GSV DOUBLE,
                Distribution_Channel STRING,
                Division STRING
            )
            USING {write_format}
            {partition_clause}
            LOCATION '{write_path}'
            TBLPROPERTIES (
                'region' = 'NA',
                'lineage' = '',
                'segment' = 'MARS MW',
                'source_system' = 'blue_yonder'
            )
        """.format(
            **output_config
        )
        primary_keys = ["unique_key"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
