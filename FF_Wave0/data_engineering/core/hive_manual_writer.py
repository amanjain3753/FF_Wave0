from collections.abc import Callable
from typing import cast

from pyspark.sql import DataFrame
from simpel.interface.writer.isparkwriter import ISparkWriter


class HiveWriterManual(ISparkWriter):
    """
    Implementation of the ISparkWriter interface for writing data to Hive tables.

    This class provides methods to write data to a Hive table using specified insertion type, partition,
    and other configurations.

    Methods:
        _type() -> str:
            Get the type of write operation (hive).

        write_data(config: dict, data: DataFrame, ddl_scripts: Optional[Callable]) -> None:
            Write data to a Hive table.

    """

    @classmethod
    def _type(cls) -> str:
        """
        Get the type of write operation (hive).

        :return: The write operation type.
        :rtype: str
        """
        return "hive_manual"

    def write_data(
        self, config: dict, data: DataFrame, ddl_scripts: Callable | None
    ) -> None:
        """
        Write data to a database table using specified insertion type and partition.

        :param config: Configuration containing table name, partition, and insert type.
        :type config: dict
        :param data: DataFrame containing the data to be written.
        :type data: pyspark.sql.DataFrame
        :param ddl_scripts: A function that provides DDL scripts and primary keys.
        :type ddl_scripts: Optional[Callable]

        :return: None.
        """
        if ddl_scripts is None:
            raise ValueError("DDL data is None")

        # To execute DDL
        self.execute_ddl(config, ddl_scripts)

        output_format = cast(str, config.get("write_format", None))
        write_mode = config.get("insert_type", None)
        table_name = config.get("table_name", None)

        writer = (
            data.write.format(output_format)
            .mode(write_mode)
            .option("partitionOverwriteMode", "dynamic")
        )

        if partition_cols := config.get("partition", None):
            writer = writer.partitionBy(partition_cols)

        writer.saveAsTable(table_name)
