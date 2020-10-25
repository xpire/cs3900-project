"""
    File name: utilities.py
    Author: Peiyu Tang
    Date created: 10/18/2020
    Python Version: 3.7.3
    Purpose: Some utility functions used by core 
        features, maybe it can be used by other modules too 
"""
import inspect
import logging
import os
from collections import defaultdict

from sqlalchemy.exc import SQLAlchemyError


def find_path_curr_f() -> str:
    """
    Find the absolute path of currently executed file
    """
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    abs_path = os.path.dirname(os.path.abspath(filename))
    return filename, abs_path


def log_msg(msg: str, level: str) -> None:
    """
    Log a message to console to indicate status for production, level can be used
    are {DEBUG < INFO < WARNING < ERROR < CRITICAL}. Please note that this only
    handles printing not actually raising any errors
    """
    logger = logging.getLogger("backend logger")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    plvs = defaultdict(lambda: None)
    log_lvs = {
        "DEBUG": logger.debug,
        "INFO": logger.info,
        "WARNING": logger.warning,
        "ERROR": logger.error,
        "CRITICAL": logger.critical,
    }

    for key, item in log_lvs.items():
        plvs[key] = item

    if plvs[level] == None:
        logger.critical("No specified logger level.")
    else:
        plvs[level](msg)


def fail_save(func):
    """
    Handle update crud operation using this, prevents backend from stopping.
    """

    def inner(*args, **kwargs):
        ret = None
        try:
            ret = func(*args, **kwargs)
            return ret
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            log_msg(error, "ERROR")
            return None

    return inner
