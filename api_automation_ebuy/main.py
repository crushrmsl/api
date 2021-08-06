# -*- coding: utf-8 -*-

import unittest
import os
import time

from library.HTMLTestRunnerNew import HTMLTestRunner
from common.constant import CASE_DIR, REPORT_DIR
from common.send_email import SendEmail


_title = '自动化测试脚本'
_description = '接口自动化项目测试报告'
_tester = '蒋世芳'
report_name = 'report.html'
report_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_" + report_name
mail_title = '自动化测试报告'
mail_message = '这是自动化测试报告，请查收'
file_path = os.path.join(REPORT_DIR, report_name)

# 创建测试集合
suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

with open(file_path, 'wb') as f:
    runner = HTMLTestRunner(
        stream=f,
        verbosity=2,
        title=_title,
        description=_description,
        tester=_tester
    )
    runner.run(suite)


# 发送email
SendEmail.send_qq_file_mail(mail_title, mail_message, file_path, report_name)
