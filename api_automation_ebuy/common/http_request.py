# -*- coding: utf-8 -*-


import time
import requests
from requests.sessions import Session
from common.logger import output_log
from common.constant import REPORT_DIR

"""
封装requests类，根据用例中的请求方法，来决定发起什么类型的请求。输出logging日志
"""


class HTTPRequest(object):
    """记录cookies信息给下一次请求使用"""

    def __init__(self):
        self.session = Session()

    def request(self, method, url,
                params=None, data=None,
                headers=None, cookies=None, json=None, **kwargs):
        method = method.lower()
        # 如果请求没有携带headers 则自定义一个headers 加到请求中
        if headers is None:
            headers = {'User-Agent': 'Apache-HttpClient/4.5.12 (Java/1.8.0_261)'}
        # 如果请求携带了headers 但是headers中没有User-Agent 则设置默认的User-Agent
        if headers.get('User-Agent') is None:
            headers['User-Agent'] = 'Apache-HttpClient/4.5.12 (Java/1.8.0_261)'
        if method == "post":
            # 判断是否使用json来传参（适用于接口项目有使用json传参）
            if json:
                output_log.info(f"正在发送请求,地址:{url},方法:{method},参数:{json},类型:json,请求头:{headers}")
                return self.session.post(url=url, json=json, headers=headers, cookies=cookies, **kwargs)
            else:
                output_log.info(f"正在发送请求,地址:{url},方法:{method},参数:{data},类型:form-data,请求头:{headers}")
                return self.session.post(url=url, data=data, headers=headers, cookies=cookies, **kwargs)
        elif method == "get":
            output_log.info(f"正在发送请求,地址:{url},方法:{method},参数:{params},请求头:{headers}")
            return self.session.get(url=url, params=params, headers=headers, cookies=cookies, **kwargs)
        elif method == 'put':
            output_log.info(f"正在发送请求,地址:{url},方法:{method},参数:{json},请求头:{headers}")
            return self.session.put(url=url, json=json, headers=headers, cookies=cookies, **kwargs)
        elif method == 'delete':
            output_log.info(f"正在发送请求,请求地址:{url},请求方法:{method},请求参数:{data},请求头:{headers}")
            return self.session.delete(url=url, headers=headers, cookies=cookies, **kwargs)

    def close(self):
        self.session.close()


if __name__ == '__main__':

    http = HTTPRequest()

    # url = 'http://localhost:8080/ebuy/Login'
    # data = {'loginName': 'dfsagas', 'password': '123456', 'action': 'login'}
    # response = http.request(method='post', url=url, data=data)
    # print(response.json())

    url = 'http://localhost:8080/ebuy/Register'
    data = {'loginName': 'asgasdgasdgsad', 'password': '123456', 'userName': '李易峰', 'action': 'saveUserToDatabase', 'sex': 1, 'email': '362456534@qq.com', 'mobile': '15088661122', 'identityCode': '420116198811255875'}
    response = http.request(method='post', url=url, data=data)
    print(response.json())

