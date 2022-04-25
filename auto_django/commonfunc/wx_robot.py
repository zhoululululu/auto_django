# -*- coding: utf-8 -*- 
"""
Created on 2021/9/13 13:53 
@File  : wx_robot.py
@author: zhoul
@Desc  :
"""

from auto_django.commonfunc.request_client import RequestClient
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class WeChat:

    def __init__(self, path1, path2):
        self.request = RequestClient("https://qyapi.weixin.qq.com")
        self.header = '{"Content-Type": "application/json"}'

        self.path1 = path1
        self.path2 = path2

    def send_message(self, send_result_data):
        """
        发送文案信息
        :param send_result_data:   请求文件
        :return:
        """
        # 获取企业微信群机器人的url, 使用的python第三方库requests库发送的请求
        # 发送请求报告
        res = self.request.get_request(path=self.path1, port="", method="post", json_value=send_result_data,
                                       headers=self.header,
                                       file_value='')

    def send_file(self, file):
        """
        发送文案信息
        :param file:文件
        :return:
        """
        # 获取企业微信群机器人的url, 使用的python第三方库requests库发送的请求
        # # 上传测试报告文件
        media_id = self.request.get_request(path=self.path2, port="", method="post", json_value="{}",
                                            headers=self.header,
                                            file_value=file, file_key="file")['media_id']
        #
        send_file_data = {"msgtype": "file", "file": {"media_id": media_id}}
        # # 发送测试报告文件
        send_file = self.request.get_request(path=self.path1, port="", method="post", json_value=send_file_data,
                                             headers=self.header,
                                             file_value='')

        return send_file