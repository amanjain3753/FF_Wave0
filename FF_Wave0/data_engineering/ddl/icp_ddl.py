"""DDL for the ICP (inter company price) table."""


def icp_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        icp, resolving the write path from
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
        ddl_statements = """
            CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                unique_key STRING,
                Material_Number STRING,
                Material_Description STRING,
                Sales_Org STRING,
                Distribution_Channel STRING,
                Start_Date STRING,
                End_Date STRING,
                UOM STRING,
                ICP DOUBLE
            )
            USING {write_format}
            LOCATION '{write_path}'
            TBLPROPERTIES (
                'region' = 'NA',
                'lineage' = '',
                'segment' = 'MARS MW',
                'source_system' = 'sap'
            )
        """.format(
            **output_config
        )
        primary_keys = ["unique_key"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
