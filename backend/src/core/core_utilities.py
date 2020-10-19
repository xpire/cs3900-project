"""
    File name: core_utilities.py
    Author: Peiyu Tang
    Date created: 10/18/2020
    Python Version: 3.7.3
    Purpose: Some utility functions used by core 
        features, maybe it can be used by other modules too 
"""
import inspect
import os


def find_path_curr_f() -> str:
    """
    Find the absolute path of currently executed file
    """
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    abs_path = os.path.dirname(os.path.abspath(filename))
    return filename, abs_path
