from setuptools import find_packages, setup

INSTALL_REQUIRES = []

setup(
    name="FF_Wave0",
    python_requires=">=3.9",
    packages=find_packages(exclude=["test", "test.*"]),
    version="2.1.5-alpha",
    description="",
    author="",
    entry_points={
        "console_scripts": [
            "run_etl = FF_Wave0.data_engineering.main.entry_point:main"
        ]
    },
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.conf', '*.json'],
        # And include any *.msg files found in the 'hello' package, too:

    }
)
