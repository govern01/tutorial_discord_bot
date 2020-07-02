# For creating log files
import os
# Logging interface
import logging
from logging import FileHandler
from logging import Formatter
# For file name
from datetime import datetime

# Global level variables
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
LOG_FILE_PATH = "./logs/"


def generate_logger():
    """Generates a logger with a file handler

    This function generates a logger with file_handler so we can save chat logs to a file over printing to console or
    other options. The log file is in the format of {currentdate}_{counter}.log, the counter increments if the bot has
    been started more than once in a day.

    :return logger: A logger object
    """
    # Check if the logs directory is here
    if not os.path.isdir(LOG_FILE_PATH):
        os.mkdir(LOG_FILE_PATH)

    logger = logging.getLogger("chat_log")
    logger.setLevel(LOG_LEVEL)

    datestr = datetime.now().strftime("%d-%m-%Y")
    counter = 0
    file_name = f"{datestr}_{counter}"
    file_path = f"{LOG_FILE_PATH}{file_name}.log"
    while os.path.isfile(file_path):
        counter += 1
        file_name = f"{datestr}_{counter}"
        file_path = f"{LOG_FILE_PATH}{file_name}.log"

    logger_handler = FileHandler(file_path)
    logger_handler.setLevel(LOG_LEVEL)
    logger_handler.setFormatter(Formatter(LOG_FORMAT))

    logger.addHandler(logger_handler)
    return logger
