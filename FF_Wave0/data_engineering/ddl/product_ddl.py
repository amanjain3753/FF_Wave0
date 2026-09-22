"""DDL for the SAP product masterdata table."""


def product_masterdata_ddl(output_config):
    """
    summary: Builds the CREATE EXTERNAL TABLE DDL statement for
        product_masterdata, resolving the write path from
        output_config.

    parameters:
        output_config:
            datatype: dict
            description: Output configuration containing table_name, data_base,
                write_path and write_format.
    return:
        datatype: dict
        description: Dictionary with keys primary_keys (["Material_SKU"]) and
            ddl_statements (the rendered CREATE EXTERNAL TABLE statement).
    """
    full_table_name = output_config.get("table_name")

    catalog = full_table_name.split(".")[0]
    schema = full_table_name.split(".")[1]
    table = full_table_name.split(".")[2]

    if full_table_name == f"{catalog}.{schema}.{table}":
        ddl_statements = """
            CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                Material_SKU STRING,
                Material_Desc STRING,
                Material_Type STRING,
                Marked_For_Deletion STRING,
                ZREP STRING,
                ZREP_Desc STRING,
                EAN STRING,
                Base_UOM STRING,
                Traded_Unit_Format BIGINT,
                Traded_Unit_Format_Desc STRING,
                Weight_Unit STRING,
                Gross_Weight DECIMAL(18,3),
                Net_Weight DECIMAL(18,3),
                Business_Segment_Id BIGINT,
                Business_Segment_Desc STRING,
                Market_Segment BIGINT,
                Brand_Flag BIGINT,
                Brand_Flag_Desc STRING,
                Brand_Sub_Flag BIGINT,
                Brand_Sub_Flag_Desc STRING,
                Multipack_Quantity BIGINT,
                Multipack_Quantity_Desc STRING,
                Product_Pack_Size_Group BIGINT,
                Product_Pack_Size_Group_Desc STRING,
                Consumer_Pack_Type BIGINT,
                Consumer_Pack_Type_Desc STRING,
                Product_Pack_Size STRING,
                Product_Category STRING,
                Product_Type BIGINT,
                Traded_Unit_Configuration BIGINT,
                Traded_Unit_Configuration_Desc STRING,
                EC_Group INT,
                EC_Group_Description STRING,
                Product_Segment STRING,
                Product_Segment_Description STRING,
                Product_Sub_Segment STRING,
                Product_Sub_Segment_Description STRING
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
        primary_keys = ["Material_SKU"]

    else:
        raise Exception(f"DDL script for table {full_table_name} not found")

    return {"primary_keys": primary_keys, "ddl_statements": ddl_statements}
