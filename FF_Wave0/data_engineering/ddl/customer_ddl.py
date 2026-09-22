"""DDL for the SAP customer masterdata table."""


def customer_masterdata_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        customer_masterdata, resolving the write path from
        output_config.

    parameters:
        output_config:
            datatype: dict
            description: Output configuration containing table_name, data_base,
                write_path and write_format.
    return:
        datatype: dict
        description: Dictionary with keys primary_keys (["Code"]) and
            ddl_statements (the rendered CREATE EXTERNAL TABLE statement).
    """
    full_table_name = output_config.get("table_name")

    catalog = full_table_name.split(".")[0]
    schema = full_table_name.split(".")[1]
    table = full_table_name.split(".")[2]

    if full_table_name == f"{catalog}.{schema}.{table}":
        ddl_statements = """
            CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                `Code` STRING,
                `Customer` STRING,
                `Customer Desc` STRING,
                `Marked_For_Deletion` STRING,
                `Sales Org` STRING,
                `Distribution Channel` STRING,
                `Division` STRING,
                `Sold-To` STRING,
                `Sold-To Desc` STRING,
                `Payer` STRING,
                `Payer Desc` STRING,
                `Ship-To` STRING,
                `Ship-To Desc` STRING,
                `Demand Group` STRING,
                `Demand Group Desc` STRING,
                `Price List` STRING
            )
            USING {write_format}
            LOCATION '{write_path}'
            TBLPROPERTIES (
                'delta.columnMapping.mode'='name',
                'delta.minReaderVersion'='2',
                'delta.minWriterVersion'='5',
                'region' = 'NA',
                'lineage' = '',
                'segment' = 'MARS MW',
                'source_system' = 'sap'
            )
        """.format(
            **output_config
        )
        primary_keys = ["Code"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
