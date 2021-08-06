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
from common.tools import check_login


file_name = 'api_automation_ebuy.xlsx'

@ddt
class RegisterTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "register")
    cases = wb.read_line_data()

    @classmethod
    def setUpClass(cls) -> None:
        output_log.info("============================== 开始执行注册接口测试 ==============================")
        cls.http = HTTPRequest()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls) -> None:
        output_log.info("============================== 注册接口测试执行完毕 ==============================")
        cls.http.close()
        cls.db.close()

    @data(*cases)  # 拆包，拆成几个参数
    def test_register(self, case):

        # 拼接url地址
        url = 'http://localhost:8080' + case.url
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

        time.sleep(3)

        request_data = eval(case.request_data)

        # 注册成功的用例 查询数据库 登录 断言
        if '正常注册' in case.title:
            login_name = request_data.get('loginName')
            username = request_data.get('userName')
            sql = f'select userName from easybuy_user where loginName="{login_name}";'
            db_res = self.db.find_one(sql)
            db_username = db_res.get('userName')

            login_msg = check_login(request_data)
         # 非正常注册用例 此3个断言失效
        else:
            username = request_data.get('userName')
            db_username = username
            login_msg = '登陆成功！'

        try:
            self.assertEqual(eval(case.expected_data), res)
            self.assertEqual(username, db_username)
            self.assertEqual(login_msg, '登陆成功！')
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
