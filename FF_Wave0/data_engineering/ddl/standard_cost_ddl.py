"""DDL for the standard cost table."""


def standard_cost_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        standard_cost, resolving the write path from
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
                Code STRING,
                Company_Code STRING,
                Plant STRING,
                Material_Number STRING,
                Cost_Component BIGINT,
                Costing_Status STRING,
                Unit_of_Measure STRING,
                Currency STRING,
                Cost_Per_Case DOUBLE,
                Lot_Size INT,
                Costing_Date_From STRING,
                Costing_Date_To STRING,
                Material_Type STRING,
                Cost_Component_Description STRING,
                Material_Description STRING,
                Net_Weight DOUBLE,
                Base_Unit STRING,
                Cost_Per_Tonne DOUBLE
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
        primary_keys = ["Code"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
