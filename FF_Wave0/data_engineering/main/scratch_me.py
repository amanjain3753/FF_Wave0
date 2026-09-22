# Databricks notebook source

# %load_ext autoreload
# %autoreload 2

# COMMAND ----------

# ## if running from databricks workspace folder uncomment the below cell content

# def updated_databricks_preamble():
#     import os
#     import sys
#
#     cwd = os.getcwd()
#     notebook_entrypoint = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
#
#     new_cwd = "/Workspace" + notebook_entrypoint.rsplit("/",1)[0]
#     path_add = "/Workspace" + notebook_entrypoint.rsplit("/",4)[0]
#
#     if cwd != new_cwd:
#         os.chdir(new_cwd)
#         print(f"setting current working directory to be {new_cwd}")
#
#     if path_add not in sys.path:
#         sys.path.append(path_add)
#         print(f"adding the following path to sys path {path_add}")
#
#
# try:
#     updated_databricks_preamble()
#     del updated_databricks_preamble
# except Exception as e:
#     print("exception while running preamble", str(e))



# COMMAND ----------

import sys

from pathlib import Path
from simpel.logger.logging import LoggingManager as lm
from simpel.core.execution_manager import ExecutionManager
from simpel.utils.config import Config
from FF_Wave0.data_engineering.data_processing.dags.dags_config import PROCESS


if __name__ == "__main__":

      sys.argv = ["scratch_me.py",'--process_name', 'TEST_PROCESS2', '--environment', 'DEV']
      # sys.argv = ["scratch_me.py",'--process_name', 'TEST_PROCESS1', '--environment', 'DEV','--process_date','20230901']


      current_path = str(Path().absolute())
      default_config_dir = Config.get_config_location('FF_Wave0', current_path,
                                                      '/FF_Wave0/data_engineering/config/')
      plugin_core_dir = Config.get_config_location('FF_Wave0', current_path, '/FF_Wave0/data_engineering/core/')

      (
            ExecutionManager('FF_Wave0')
            .set_log_level(lm.INFO)
            .set_conf_paths(project_conf=default_config_dir + 'project_config.json'
                            , env_conf=default_config_dir + 'env.json'
                            )
            .set_logging_conf(default_config_dir + 'logging.conf')
            .set_process_definition(PROCESS)
            .register(plugin_core_dir)
            .run()
      )



