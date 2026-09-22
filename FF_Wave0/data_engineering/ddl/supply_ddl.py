"""DDL for the supply table."""


def supply_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        supply, resolving the write path from
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
        output_config["partition"] = ", ".join(output_config["partition"])
        ddl_statements = """
            CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                unique_key STRING,
                Demand_Type STRING,
                Part_Site STRING,
                Destination_Site STRING,
                Material_Number STRING,
                Material_Description STRING,
                ZREP STRING,
                Fiscal_year_period STRING,
                volume_cases DOUBLE,
                volume_tonnes DOUBLE,
                Sales_org STRING
            )
            USING {write_format}
            PARTITIONED BY ({partition})
            LOCATION '{write_path}'
            TBLPROPERTIES (
                'region' = 'NA',
                'lineage' = '',
                'segment' = 'MARS MW',
                'source_system' = 'kinaxis'
            )
        """.format(**output_config
        )
        primary_keys = ["unique_key"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
