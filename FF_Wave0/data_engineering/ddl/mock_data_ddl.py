def mock_data_ddl(output_config):
    table_name=output_config.get('table_name')
    if 'mock_mars_calendar' in table_name:
        ddl_statements= """
        CREATE external TABLE if not exists {table_name} (
        STARTDATE VARCHAR(20),
        MARS_PRD VARCHAR(20),
        MARS_YRPD VARCHAR(20),
        YRPRD_STARTDT VARCHAR(20)
        )
        USING {write_format}
        LOCATION '{write_path}'
        TBLPROPERTIES (
          'region' = 'GlobaL',
          'segment' = 'PetNutrition')
        """.format(**output_config)
        primary_keys='STARTDATE'
    else:
        raise 'DDL script for table {table_name} not found'.format('table_name',table_name)
    return {
        'primary_keys': primary_keys,
        'ddl_statements': ddl_statements
    }
