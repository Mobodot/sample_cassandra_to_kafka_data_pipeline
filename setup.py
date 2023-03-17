from typing import List
from setuptools import setup, find_packages

__VERSION__ = "0.0.0"

SRC_REPO = "sample_cassandra_to_kafka_data_pipeline"
AUTHOR_NAME = "Mobodot"
AUTHOR_EMAIL = "mobosomto@gmail.com"

setup(
    name=SRC_REPO,
    version=__VERSION__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description=("A streaming data pipeline project "\
                "connecting CASSANDRA to KAFKA using spark"),
    package_dir={"": "src"},
    packages=find_packages(where="src")
                
)
