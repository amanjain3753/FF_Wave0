from simpel.interface.dao import IJobDAO
from FF_Wave0.data_engineering.data_processing.feature.feature_sql import  test_feature_impl


def test_transform_sql(jobDAO: IJobDAO, process_date: str):
    logger = jobDAO.logger
    jobDAO.logger.info(jobDAO.args)
    logger.info("test_transform_sql")
    logger.info(process_date)
    return_dict = test_feature_impl(jobDAO.data_dict, logger)
    return return_dict
