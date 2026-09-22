from logging import Logger
from simpel.utils.dataframe_utils import DataframeUtils


def mock_feature(data_dict: dict, logger: Logger):
    logger.info("mock_feature")
    data_dict["mars_calendar"] = DataframeUtils.deduplicate_dataframe(
        data_dict["mars_calendar"]
    )
    return data_dict
