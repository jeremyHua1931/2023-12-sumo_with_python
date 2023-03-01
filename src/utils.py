# -*- encoding: utf-8 -*-
"""
@File    :   utils.py
@Contact :   jeremyhua@foxmail.com

@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/1 23:26   HuaZhangzhao    1.0          None
"""
import pytz
from datetime import datetime


def get_datetime():
    """

    Returns:

    """
    utc_now = pytz.utc.localize(datetime.now())
    current_dt = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    daytime = current_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return daytime


def _flatten_list(_2d_list):
    """

    Args:
        _2d_list:

    Returns:

    """
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list
