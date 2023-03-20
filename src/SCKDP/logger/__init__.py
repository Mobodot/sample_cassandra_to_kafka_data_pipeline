import os
import sys
from datetime import datetime
import logging as logger


def get_current_timestamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.logs"

LOG_STR = "[%(asctime)s]:: %(levelname)s:: %(message)s"
LOG_FILE_NAME = get_current_timestamp()
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)


os.makedirs(LOG_DIR, exist_ok=True)


logger.basicConfig(
                   level=logger.INFO,
                   format=LOG_STR,
                   handlers=[
                       logger.FileHandler(LOG_FILE_PATH),
                       logger.StreamHandler(sys.stdout)
                   ])
