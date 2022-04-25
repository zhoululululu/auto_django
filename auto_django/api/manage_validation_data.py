# -*- coding: utf-8 -*- 
"""
Created on 2021/11/18 9:30 
@File  : manage_validation_data.py
@author: zhoul
@Desc  :
"""
import json
from rest_framework.views import APIView
from auto_django.commonfunc.get_logging import Logging
from django.http import FileResponse, HttpResponse
from auto_django.commonfunc.datetime_tool import DateTimeTool
from auto_django.models import TValidationTestCase

logger = Logging()


class GetValidationData(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        page_index = json.loads(request.body).get("page_index")
        page_size = json.loads(request.body).get("page_size")
        result = {"data": [], "page_total": 0}
        try:
            validation_test_case = TValidationTestCase.objects.all()
            for validation_test_info in validation_test_case[(page_index - 1) * page_size:]:
                result["data"].append(validation_test_info.to_dict())
            result["page_total"] = len(validation_test_case)
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


class AddValidationData(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        ele = json.loads(request.body).get("ele")
        desc = json.loads(request.body).get("desc")
        service = json.loads(request.body).get("service")
        test_data = json.loads(request.body).get("test_data")
        check_data = json.loads(request.body).get("check_data")
        exp_data = json.loads(request.body).get("exp_data")
        exp_desc = json.loads(request.body).get("exp_desc")
        result = {}
        try:
            TValidationTestCase.objects.create(desc=desc, ele=ele, service=service, request_data=test_data,
                                               check_type=check_data, check_data=exp_data, exp_data=exp_desc,
                                               create_user="test", create_time=DateTimeTool.get_now_time(), is_active=1)
            result = {"statusCode": 0, "message": "新增validation数据成功"}
        except Exception as e:
            logger.error("获取数据出错： %s" % e)
            result = {"statusCode": 10000, "message": "新增validation数据失败"}
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


class EditValidationData(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        ele = json.loads(request.body).get("ele")
        desc = json.loads(request.body).get("desc")
        service = json.loads(request.body).get("service")
        test_data = json.loads(request.body).get("test_data")
        check_data = json.loads(request.body).get("check_data")
        exp_data = json.loads(request.body).get("exp_data")
        exp_desc = json.loads(request.body).get("exp_desc")
        result = {}
        try:
            TValidationTestCase.objects.filter(id=id).update(desc=desc, ele=ele, service=service,
                                                             request_data=test_data,
                                                             check_type=check_data, check_data=exp_data,
                                                             exp_data=exp_desc,
                                                             create_user="test",
                                                             create_time=DateTimeTool.get_now_time(), is_active=1)
            result = {"statusCode": 0, "message": "新增validation数据成功"}
        except Exception as e:
            logger.error("获取数据出错： %s" % e)
            result = {"statusCode": 10000, "message": "新增validation数据失败"}
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


class DeleteValidationData(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        result = {}
        try:
            TValidationTestCase.objects.filter(id=id).update(is_active=0)
            result = {"statusCode": 0, "message": "validation数据删除成功"}
        except Exception as e:
            logger.error("获取数据出错： %s" % e)
            result = {"statusCode": 10000, "message": "validation数据删除失败"}
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


class QueryValidationData(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        result = {}
        try:
            TValidationTestCase.objects.filter(id=id).update(is_active=0)
            result = {"statusCode": 0, "message": "validation数据删除成功"}
        except Exception as e:
            logger.error("获取数据出错： %s" % e)
            result = {"statusCode": 10000, "message": "validation数据删除失败"}
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
