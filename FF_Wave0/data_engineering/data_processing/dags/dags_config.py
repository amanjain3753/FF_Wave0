from FF_Wave0.data_engineering.data_processing.dags.dag_mock_data import mock_transform
from FF_Wave0.data_engineering.ddl.mock_data_ddl import mock_data_ddl

"""
Demonstration of Simpel ETL Process Orchestration

This script demonstrates how to orchestrate and execute ETL (Extract, Transform, Load) processes
using the Simpel framework. It showcases the usage of the PROCESS dictionary to define and manage
different ETL processes.

Usage:
    1. Ensure that the required modules and classes are imported.
    2. Modify the PROCESS dictionary to define your ETL processes, transformations, and DDL scripts.
    3. Run the script to execute the ETL processes.

Prerequisites:
    - Simpel framework is installed.
    - Required transformation functions (test_transform_1, test_transform_2) and DDL scripts
      (test_create_dll_1, test_create_dll_2) are available in the respective modules.
    - Each ETL process should have a corresponding transformation and DDL script defined.

PROCESS Dictionary:
    The PROCESS dictionary defines the ETL processes along with their associated transformations and DDL scripts.
    Each process is identified by a unique key, and the dictionary structure is as follows:

    'PROCESS_NAME': {
        'transform': transform_function,  # Specify the transformation function for this process
        'ddl': ddl_script_function        # Specify the DDL script function for this process
    }

    Consolidated Process:
    To consolidate multiple processes, you can create a consolidated process entry. In this case, the key
    points to a list of individual process names that should be executed sequentially. For example:

    'CONSOLIDATED_PROCESS_NAME': ['PROCESS_NAME1', 'PROCESS_NAME2']

Steps:
1. Import the required transformation functions and DDL scripts.
2. Define the PROCESS dictionary to configure the ETL processes and their associated functions.
3. Run the script to execute the defined ETL processes. Each process will go through the following steps:
   a. Execute the transformation function.
   b. Execute the DDL script function.

Note:
- Ensure that the transformation functions and DDL scripts are correctly implemented in the respective modules.
- Modify the PROCESS dictionary to match the processes you want to execute.
- You can add more processes by following the same dictionary structure.
- The script showcases the basic usage of Simpel's process orchestration capabilities.

Author: Simpel Governance Team
Date: 25-08-2023
"""

PROCESS = {
    "MOCK_DATA": {"transform": mock_transform, "ddl": mock_data_ddl}
}
