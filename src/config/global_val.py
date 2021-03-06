#!/usr/bin/python
# -*- coding: utf-8 -*-


def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, def_value=None):
    try:
        return _global_dict[key]
    except KeyError:
        return def_value
