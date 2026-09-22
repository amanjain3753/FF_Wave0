from pathlib import Path

from simpel.logger.logging import LoggingManager as lm
from simpel.core.execution_manager import ExecutionManager
from simpel.utils.config import Config
from FF_Wave0.data_engineering.data_processing.dags.dags_config import PROCESS



if __name__ == '__main__':
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
