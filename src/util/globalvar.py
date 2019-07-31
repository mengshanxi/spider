#!/usr/bin/python
# -*- coding: utf-8 -*-


def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name):
    try:
        return _global_dict.get(name)
    except KeyError:
        return "KeyError"


def remove(name):
    del _global_dict[name]


def check_by_task(task_id):
    return get_value(task_id) is not None


def check_by_batch_num(batch_num):
    return batch_num in _global_dict.values()
