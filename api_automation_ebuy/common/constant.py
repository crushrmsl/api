# -*- coding: utf-8 -*-


import os


"""
封装动态获取常量，项目中使用的各种绝对路径
"""

# 获取项目目录的根路径 # 二级目录是common，一级目录（根目录)就是qcd_api_test
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 获取配置文件目录的路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')

# 获取excel数据目录的路径
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 获取日志目录的路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告目录的路径
REPORT_DIR = os.path.join(BASE_DIR, 'report')

# 获取测试用例目录的路径
CASE_DIR = os.path.join(BASE_DIR, 'test_cases')


if __name__ == '__main__':
    print(CASE_DIR)
    file_path = os.path.join(CASE_DIR, 'test_login.py')
    print(os.path.isdir(CASE_DIR))
    print(os.path.isfile(CASE_DIR))

    print(os.path.isdir(file_path))
    print(os.path.isfile(file_path))
