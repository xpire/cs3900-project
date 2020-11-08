"""
    File name: utilities.py
    Author: Peiyu Tang
    Date created: 10/18/2020
    Python Version: 3.7.3
    Purpose: Some utility functions used by core 
        features, maybe it can be used by other modules too 
"""
import csv
import datetime as dt
import inspect
import logging
import os
from collections import defaultdict
from enum import Enum
from os import path
from typing import Dict, List

from fastapi import HTTPException
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

HTTP400 = lambda detail: HTTPException(status_code=400, detail=detail)
Const = lambda x: Field(x, const=x)


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


def find(iterable, default=None, **kwargs):
    """
    Find the first element in the iterable whose attribute values match
    those specified by the keyword arguments
    """

    def is_match(x):
        try:
            for name, value in kwargs.items():
                if getattr(x, name) != value:
                    return False
            return True
        except AttributeError:
            return False

    return next((x for x in iterable if is_match(x)), default)


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
    if not logger.handlers:
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
            log_msg(str(e._message), "ERROR")
            return None

    return inner

    # Modified based on https://stackoverflow.com/questions/35241643/convert-datetime-time-into-datetime-timedelta-in-python-3-4


def as_delta(time: dt.time):
    return dt.datetime.combine(dt.datetime.min, time) - dt.datetime.min


def db_uri_generator(*, proj_root: str, db_name: str) -> str:
    """
    Generate the URI that sqlalchemy uses for db connection.'
    """
    return "sqlite:///" + os.path.join(proj_root, "database", db_name + ".sqlite3")


def ret_initial_users(proj_root: str) -> List[Dict]:
    """
    Insert the initial users
    """
    with open(path.join(proj_root, "database", "initial_users.csv"), mode="r") as file:
        return [sd for sd in csv.DictReader(file)]
