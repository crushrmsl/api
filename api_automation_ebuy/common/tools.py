# -*- coding: utf-8 -*-


import random
import time

from common.http_request import HTTPRequest


def check_login(request_data):
    http = HTTPRequest()
    url = 'http://localhost:8080' + "/ebuy/Login"
    data = {'loginName': request_data.get('loginName'), 'password': request_data.get('password'), 'action': 'login'}
    response = http.request(method="post", url=url, data=data)
    result = response.json()["data"]
    http.close()
    print("")
    print("登录请求参数--> {}".format(request_data))
    print("登录返回结果--> {}".format(response.json()))
    time.sleep(1)
    return result
