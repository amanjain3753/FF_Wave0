from simpel.interface.dao import IJobDAO
from FF_Wave0.data_engineering.data_processing.constants import MOCK_DATA
from FF_Wave0.data_engineering.data_processing.feature.feature_mock_data import mock_feature


def mock_transform(jobDAO: IJobDAO, process_date: str):
    logger = jobDAO.logger
    jobDAO.logger.info(jobDAO.args)
    logger.info(f"Recommended to use one constant dict for one process{MOCK_DATA['CONSTANT_1']}")
    logger.info(f"Default process date: {process_date}")
    return_dict = mock_feature(jobDAO.data_dict, logger)
    return return_dict
