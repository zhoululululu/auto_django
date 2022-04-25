# -*- coding: utf-8 -*- 
"""
Created on 2021/11/18 15:03 
@File  : manage_tracking_number.py
@author: zhoul
@Desc  :
"""

import json
from rest_framework.views import APIView
from auto_django.commonfunc.get_logging import Logging
from django.http import HttpResponse
from auto_django.business.generate_tracking_number import GenerateTrackingNumber
from auto_django.models import TGenerateTrackingNumber

logger = Logging()


class GenerateTrackingNumberAPI(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        result = {"data": []}
        env = json.loads(request.body).get("env")
        product = json.loads(request.body).get("product")
        num = json.loads(request.body).get("num")
        try:
            if type(num) is int:
                tracking_number_list = GenerateTrackingNumber().generate_tracking_num(env, product, num=int(num))
                for i in tracking_number_list:
                    result["data"].append({"tracking_number": i})
                    TGenerateTrackingNumber.objects.create(env=env, product=product,
                                                           tracking_number=i,
                                                           create_user="test")
            else:
                result["data"].append({"tracking_number": "数量请输入正整数"})
        except Exception as e:
            result["data"].append({"tracking_number": "请检查数据"})
            logger.error("获取订单号出错： %s" % e)
        response = HttpResponse(
            json.dumps(result),
            content_type="application/json")
        response["Access-Control-Allow-Methods"] = "*"
        response["Access-Control-Allow-Origin"] = ['*']
        return response

    @staticmethod
    def options(request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Method'] = request.method
        response['Access-Control-Allow-Origin'] = ['*']
        response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type"
        return response


class GetTrackingNumberAPI(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        page_index = json.loads(request.body).get("page_index")
        page_size = json.loads(request.body).get("page_size")
        result = {"data": [], "page_total": 0}
        try:
            generate_tracking_number = TGenerateTrackingNumber.objects.all().order_by(
                "-create_time")
            for tracking_info in generate_tracking_number[(page_index - 1) * page_size:page_index * page_size]:
                result["data"].append(tracking_info.to_dict())
            result["page_total"] = len(generate_tracking_number)
        except Exception as e:
            logger.error("获取数据出错： %s" % e)
            result["data"] = {"error": "请求出错"}
        response = HttpResponse(
            json.dumps(result),
            content_type="application/json")
        response["Access-Control-Allow-Methods"] = "*"
        response["Access-Control-Allow-Origin"] = ['*']
        return response

    @staticmethod
    def options(request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Method'] = request.method
        response['Access-Control-Allow-Origin'] = ['*']
        response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type"
        return response
