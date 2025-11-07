#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: util/class_.py
#
# 通用类库
#

import os
import json as json_module
from configparser import RawConfigParser
import logging


basedir = os.path.join(os.path.dirname(__file__), "../")


__all__ = [
    "Config",
    "Logger",
]


class Config(object):
    """[配置文件类，支持JSON格式配置文件]

    Attributes:
        class:
            Config_File    str    配置文件绝对路径（config.json）
        instance:
            __config       dict   JSON 配置数据
    """

    Config_File = os.path.abspath(os.path.join(basedir, "config.json"))

    def __init__(self):
        self.__config = {}
        self._load_config()

    def _load_config(self):
        """加载 JSON 配置文件"""
        if os.path.exists(self.Config_File):
            with open(self.Config_File, "r", encoding="utf-8-sig") as f:
                self.__config = json_module.load(f)
        else:
            raise FileNotFoundError(f"配置文件未找到: {self.Config_File}")

    def __getitem__(self, idx):
        """config[] 操作运算的封装"""
        return self.__config.get(idx, {})

    def sections(self):
        """返回所有的 section 名称"""
        return [key for key in self.__config.keys() if key != "_comment"]

    def get(self, section, key):
        """获取字符串类型的配置值"""
        if section not in self.__config:
            raise ValueError(f"section [{ section}] not found !")
        if key not in self.__config[section]:
            raise ValueError(f"key '{key}' in section [{section}] is missing !")
        return self.__config[section][key]

    def getint(self, section, key):
        """获取整数类型的配置值"""
        value = self.get(section, key)
        if isinstance(value, int):
            return value
        return int(value)

    def getfloat(self, section, key):
        """获取浮点数类型的配置值"""
        value = self.get(section, key)
        if isinstance(value, (int, float)):
            return float(value)
        return float(value)

    def getboolean(self, section, key):
        """获取布尔类型的配置值"""
        value = self.get(section, key)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'on')
        return bool(value)


class Logger(object):
    """[日志类，logging 模块的封装]

    Attributes:
        class:
            Default_Name     str                    缺省的日志名
            config           Config                 配置文件类实例
        instance:
            logger           logging.Logger         logging 的 Logger 对象
            level            int                    logging.level 级别
            format           logging.Formatter      日志格式
            console_headler  logging.StreamHandler  控制台日志 handler
    """

    Default_Name = __name__
    config = Config()

    def __init__(self, name=None):
        self.logger = logging.getLogger(name or self.Default_Name)
        self.level = logging.DEBUG if self.config.getboolean("Base", "debug") else logging.INFO
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.console_headler)

    @property
    def console_headler(self):
        console_headler = logging.StreamHandler()
        console_headler.setLevel(self.level)
        console_headler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s, %(asctime)s, %(message)s", "%Y-%m-%d %H:%M:%S"))
        return console_headler

    """
        以下是对 logging 的五种 level 输出函数的封装
        并定义 __call__ = logging.info
    """

    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.logger.critical(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.info(*args, **kwargs)
