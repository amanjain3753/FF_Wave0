from simpel.test.unit_test import PySparkTestCase
from pyspark_test import assert_pyspark_df_equal
from FF_Wave0.data_engineering.data_processing.feature.feature_mock_data import mock_feature
import pandas as pd

class TestSample(PySparkTestCase):

    def setUp(self):
        self.logger.info("\nRunning setUp method...")
        self.mock_path = "FF_Wave0/test/data/mock/sample_feature/"
        self.expected_path = "FF_Wave0/test/data/expected/sample_feature/"

    def tearDown(self):
        self.logger.info("Running tearDown method...")

    def test_features(self):
        mars_calander = self.spark_util.read_data(self.mock_path + 'mars_cal.csv', ',', 'csv')
        data_dict = {
            'mars_calendar': mars_calander
        }
        mars_calander_op = self.spark_util.read_data(self.expected_path + 'mars_cal.csv', ',', 'csv')
        data_dict = mock_feature(data_dict, self.logger)
        assert_pyspark_df_equal(data_dict['mars_calendar'], mars_calander_op)
