from simpel.interface.reader.isparkreader import ISparkReader


class HiveReader(ISparkReader):

    @classmethod
    def _type(cls) -> str:
        return 'hive_scdp'

    def read_data(self,input:dict) :
        """
            Read data from a database table using the specified table name and condition.
            Args:
                input (dict): Dictionary containing table name and input condition.
            Returns:
                pyspark.sql.DataFrame: DataFrame containing the retrieved data.
        """
        print(self.get_process_date())
        table_name = input.get('table_name')
        where_con = input.get('input_condition')
        table_df = self.spark.sql("""select * from {0} {1}""".format(table_name, where_con))
        return table_df
