#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: util/error.py
#
# 通用错误类
#

__all__ = [
    "ConfigError",
    "APPTypeError",
    "RecordTypeError",
    "RecordNumberError",
]


class ConfigError(Exception):
    """配置文件错误"""

    pass


class APPTypeError(ConfigError):
    """不支持的跑步软件类型"""

    pass


class RecordTypeError(ConfigError):
    """不支持的记录类型"""

    pass


class RecordNumberError(ConfigError):
    """无效的记录编号"""

    pass
