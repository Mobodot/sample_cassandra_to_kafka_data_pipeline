from setuptools import setup, find_packages

__VERSION__ = "0.0.0"

SRC_REPO = "src"
AUTHOR_NAME = "Mobodot"
AUTHOR_EMAIL = "mobosomto@gmail.com"

setup(
    name=SRC_REPO,
    version=__VERSION__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description=("A small data pipeline connecting "\
                "comprising of CASSANDRA-KAFKA"),
    package_dir={"": "src"},
    packages=find_packages(where="src")
                
)
