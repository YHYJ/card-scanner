#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2019-03-28 08:52:02


"""

from logging.config import dictConfig


def set_log(log_conf: dict):
    """set log

    :log_conf: dict: config info

    """
    dictConfig(log_conf)
