#! /usr/bin/python
# encoding:utf-8
import time
import os

'''
    zip a whole directory and its sub directories and files
'''
'''os.walk()可以得到一个三元tupple(dirpath, dirnames, filenames)，其中第一个为起始路径，
第二个为起始路径下的文件夹，第三个是起始路径下的文件。'''

import os, zipfile
from os.path import join


def zipfolder(foldername, filename):
    print
    foldername
    empty_dirs = []
    zip = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(foldername):
        print
        root, dirs, files
        # 筛选空目录
        empty_dirs.extend(dir for dir in dirs if os.listdir(join(root, dir)) == [])
        for file in files:
            zip.write(join(root, file))
    for dir in empty_dirs:
        zip = zipfile.ZipFile(join(root, dir).decode("gbk" + "/"))
        zip.writestr(zip)
    zip.close()
    print
    'finish compressing %s' % zipname


if __name__ == "__main__":
    foldername = 'D:/test'
    zipname = 'D:/websp.zip'
    zipfolder(foldername, zipname)
