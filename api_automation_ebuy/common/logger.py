# -*- coding: utf-8 -*-


import logging
import os
import time
from common.constant import LOG_DIR


# 基类object
class MyLogging(object):

    # __new__ 与 __init__方法类似  一个是类开始创建时执行 一个是实例对象开始创建时执行
    # new该方法是当对象构建的时候由解释器自动回调的方法, 该方法必须"返回类的对象""
    # new方法没有通过, 那么后面的就不会进行
    def __new__(cls, *args, **kwargs):
        # 创建日志收集器
        my_log = logging.getLogger()

        # 设置收集信息级别
        my_log.setLevel('INFO')

        # 创建一个日志输出渠道，控制台
        ls = logging.StreamHandler()
        ls.setLevel('INFO')

        # 创建日志输出渠道，文件，拼接日志文件输出路径 时间戳
        cur_time = time.strftime("%Y-%m-%d %H%M", time.localtime())
        log_name = "API_Automation_{}.log".format(cur_time)
        lf = logging.FileHandler(os.path.join(LOG_DIR, log_name), encoding='utf8')
        # 设置输出级别
        lf.setLevel('INFO')

        # 将输出渠道添加到日志收集器中
        my_log.addHandler(ls)
        my_log.addHandler(lf)

        # 设置日志输出格式
        ft = '%(asctime)s - [%(filename)s -->line:%(lineno)d] - %(levelname)s : %(message)s'
        ft = logging.Formatter(ft)

        # 给输出渠道应用输出格式
        ls.setFormatter(ft)
        lf.setFormatter(ft)

        return my_log


output_log = MyLogging()


if __name__ == '__main__':
    output_log.info('正在发起请求...')



