from logging import Logger
import pyspark.sql.functions as F


def test_feature_impl(data_dict: dict, logger: Logger):
    data_dict["mars_calendar"] = data_dict["mars_calendar"].dropDuplicates(subset=["STARTDATE"])
    data_dict["mars_calendar"] = data_dict["mars_calendar"].withColumn(
        "MARS_PRD", F.when(F.col("YRPRD_STARTDT") == "202211", "P641").otherwise(F.col("MARS_PRD"))
    )
    data_dict["mars_calendar"].show(20)
    return data_dict
