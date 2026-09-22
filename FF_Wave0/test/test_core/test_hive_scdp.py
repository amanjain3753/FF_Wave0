from pyspark.sql import DataFrame
from simpel.test.unit_test import PySparkTestCase
from FF_Wave0.data_engineering.core.hive_scdp import HiveReader


class TestHiveSCDP(PySparkTestCase):

    def setUp(self):
        self.logger.info("\nRunning setUp method...")
        self.mock_path = "FF_Wave0/test/data/mock/sample_feature/"
        self.expected_path = "FF_Wave0/test/data/expected/sample_feature/"
        self.hive_reader = HiveReader()

    def tearDown(self):
        self.logger.info("Running tearDown method...")

    def test_type(self):
        assert self.hive_reader._type() == "hive_scdp"

    def test_read_data(self):
        input_data = [(1, "A"), (2, "B"), (3, "C")]
        schema = ["id", "value"]
        df = self.spark_util.create_data_frame(input_data, schema=schema)
        df.createOrReplaceTempView('mars_calander')
        input_data = {
            "table_name": "mars_calander",
            "input_condition": "where id=1"
        }
        result = self.hive_reader.read_data(input_data)
        assert result is not None
        assert isinstance(result, DataFrame)
