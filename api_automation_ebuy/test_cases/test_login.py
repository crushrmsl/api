# -*- coding: utf-8 -*-


import os
import time
import unittest

from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.logger import output_log
from common.constant import DATA_DIR, CASE_DIR
from common.http_request import HTTPRequest
from common.execute_mysql import ExecuteMysql


# 从配置获取用例excel名称
file_name = 'api_automation_ebuy.xlsx'


@ddt
class LoginTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "login")
    cases = wb.read_line_data()

    @classmethod
    def setUpClass(cls) -> None:
        output_log.info("============================== 开始执行登录接口测试 ==============================")
        cls.http = HTTPRequest()

    @classmethod
    def tearDownClass(cls) -> None:
        output_log.info("============================== 登录接口测试执行完毕 ==============================")
        cls.http.close()

    @data(*cases)  # 拆包，拆成几个参数
    def test_login(self, case):

        # 拼接url地址
        url =  "http://localhost:8080" + case.url
        # 行数等于用例编号+1
        self.row = case.case_id + 1
        # 向接口发送请求
        response = self.http.request(method=case.method, url=url, data=eval(case.request_data))
        time.sleep(2)

        # 该打印的内容会显示在报告中
        print()
        print("请求地址--> {}".format(url))
        print("请求参数--> {}".format(case.request_data))
        print("期望结果--> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        res = response.json()

        try:
            self.assertEqual(eval(case.expected_data), res)
        except AssertionError as e:
            result = 'FAIL'
            output_log.exception(e)
            raise e
        else:
            result = 'PASS'
            output_log.info("预期结果:{}, 实际结果:{}, 断言结果:{}".format(case.expected_data, res, result))
        finally:
            # 向Excel回写服务器返回结果
            self.wb.write_data(row=self.row, column=9, value=str(response.json()))
            # 向Excel回写断言结果
            self.wb.write_data(row=self.row, column=10, value=result)
