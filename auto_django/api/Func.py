# -*- coding: utf-8 -*- 
"""
Created on 2022/1/19 16:10 
@File  : Func.py
@author: zhoul
@Desc  :
"""
import pandas
from auto_django.models import TValidationTestCase
import os
from rest_framework.views import APIView
from django.http import HttpResponse
import json
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class EditData(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        result = {}
        test_data = pandas.read_excel(rootPath + "\\data\\validation-case.xlsx", sheet_name="case_manage")
        desc = test_data.get("desc").tolist()
        ele = test_data.get("ele").tolist()
        service = test_data.get("Service").tolist()
        check_data = test_data.get("check_data").tolist()
        exp_data = test_data.get("expact_data").tolist()
        exp_desc = test_data.get("expact_desc").tolist()
        json_data = test_data.get("json").tolist()
        try:
            for i in range(len(json_data)):
                TValidationTestCase.objects.filter(id=i).update(desc=desc[i], ele=ele[i], service=service[i],
                                                                request_data=json_data[i],
                                                                check_type=check_data[i], check_data=exp_data[i],
                                                                exp_data=exp_desc[i]
                                                                )
            result = {"statusCode": 0, "message": "新增validation数据成功"}
        except Exception as e:
            result = {"statusCode": 10000, "message": "新增validation数据失败"}
        response = HttpResponse(
            json.dumps(result),
            content_type="application/json")
        response["Access-Control-Allow-Methods"] = "*"
        response["Access-Control-Allow-Origin"] = ['*']
        return response
