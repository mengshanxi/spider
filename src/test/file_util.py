#! /usr/bin/python
# encoding:utf-8

import os
from config.config_load import base_filepath


class FileUtil:
    def create_path(self, path):
        is_exists = os.path.exists(base_filepath + "/" + path)
        # 判断结果
        if not is_exists:
            os.makedirs(base_filepath + "/" + path)
            print(base_filepath + "/" + path + ' 创建成功')
            return True
        else:
            print(base_filepath + "/" + path + ' 目录已存在')
            return False


if __name__ == "__main__":
    file_utl = FileUtil()
    file_utl.create_path("11")
    os.remove(base_filepath)
