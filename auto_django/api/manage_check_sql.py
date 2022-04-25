# -*- coding: utf-8 -*- 
"""
Created on 2021/12/14 15:28 
@File  : manage_check_sql.py
@author: zhoul
@Desc  :
"""

import json
from rest_framework.views import APIView
from auto_django.commonfunc.get_logging import Logging
from django.http import FileResponse, HttpResponse
from auto_django.business.check_sql import CheckSql
from auto_django.models import TCheckSql
from auto_django.commonfunc.datetime_tool import DateTimeTool
from auto_django.commonfunc.beauty_excel import beauty_format
import pandas
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

logger = Logging()


class DownloadTemplateAPI(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            filename = open(rootPath + "/data/sql_data/sql_data.xlsx", "rb")
        except Exception as e:
            logger.error("报错信息： %s" % e)
        response = FileResponse(filename)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = "attachment;filename=sql_data.xlsx"
        return response

    @staticmethod
    def options(request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Method'] = request.method
        response['Access-Control-Allow-Origin'] = ['*']
        response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type"
        return response


class UploadFileAPI(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            if request.FILES:
                check_file = request.FILES.getlist('check_file')
                dir = '..\\data\\sql_data\\'
                if not os.path.exists(os.path.dirname(dir)):
                    os.makedirs(os.path.dirname(dir))
                for f in check_file:
                    file_name = DateTimeTool.get_now_date() + "sql_data.xlsx"
                    with open(rootPath + "\\data\\sql_data\\" + file_name, 'wb') as dest:
                        for chunk in f.chunks():
                            dest.write(chunk)
            result = {"statusCode": 0, "data": "文件上传成功", "file": file_name}
        except Exception as e:
            logger.error("报错信息： %s" % e)
            result = {"statusCode": 10000, "data": "文件上传失败", "file": "error"}
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


class NewCheckSqlAPI(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        version_time = json.loads(request.body).get("version_time")
        check_file = json.loads(request.body).get("file_name")
        error_key, error_value = [], []
        try:
            final_result, data_len, tracking_number_data_list, mawb_list = CheckSql(
                rootPath + "\\data\\sql_data\\" + check_file).check_all()
            aq_status = "成功" if final_result.get("aquarius") == [] else "失败"
            rdc_status = "成功" if final_result.get("rdc") == [] else "失败"
            data_result = pandas.DataFrame(
                {"版本时间": version_time, "测试数据量（仅包括订单号）": data_len, "aq库检查结果": aq_status,
                 "rdc库检查结果": rdc_status},
                index=[0])
            check_result_file = version_time + "_" + "_check_sql_result.xlsx"
            writer = pandas.ExcelWriter(rootPath + "\\resultfile\\" + check_result_file)
            data_result.to_excel(writer, sheet_name="检查数据废除状态")
            for key in final_result.keys():
                if final_result.get(key):
                    for j in final_result.get(key):
                        error_key.append(key)
                        error_value.append(j)
            error_result = pandas.DataFrame({"数据库": error_key, "数据表": error_value})
            error_result.to_excel(writer, sheet_name="废除失败表")
            if tracking_number_data_list:
                test_tracking_number = pandas.DataFrame({"生产订单号": tracking_number_data_list})
                test_tracking_number.to_excel(writer, sheet_name="测试订单号数据")
            if mawb_list:
                test_mawb_data = pandas.DataFrame({"生产主单号": mawb_list})
                test_mawb_data.to_excel(writer, sheet_name="测试主单号数据")
            writer.save()
            TCheckSql.objects.create(version_time=version_time, request_file=check_result_file,
                                     result_file=check_result_file,
                                     data_len=data_len,
                                     aq_status=aq_status,
                                     rdc_status=rdc_status,
                                     create_user="test", create_time=DateTimeTool.get_now_time(), is_active=1)
            result = {"statusCode": 0, "message": "执行成功，可下载详细数据查看"}
        except Exception as e:
            result = {"statusCode": 10000, "message": "执行失败，请检查数据"}
            print(e)
            logger.error("检查数据清除出错： %s" % e)
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


class GetCheckSqlDataAPI(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        page_index = json.loads(request.body).get("page_index")
        page_size = json.loads(request.body).get("page_size")
        version_time = json.loads(request.body).get("version_time")
        result = {"data": [], "page_total": 0}
        try:
            if version_time is None or version_time == "":
                sql_result = TCheckSql.objects.filter(is_active=1).order_by(
                    "-create_time")
            else:
                sql_result = TCheckSql.objects.filter(version_time=version_time, is_active=1).order_by(
                    "-create_time")
            for check_result_info in sql_result[(page_index - 1) * page_size:page_index * page_size]:
                result["data"].append(check_result_info.to_dict())
            result["page_total"] = len(sql_result)
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


class DelCheckSqlAPI(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        try:
            TCheckSql.objects.filter(id=id).update(is_active=0)
            result = {"statusCode": 0, "message": "删除成功"}
        except Exception as e:
            result = {"statusCode": 10000, "message": "删除失败"}
            print(e)
            logger.error("检查数据清除出错： %s" % e)
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


class DownloadResultAPI(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        result = []
        try:
            sql_result = TCheckSql.objects.filter(id=id)
            for re in sql_result:
                result.append(re.to_dict().get("result_file"))
            final_file = open(rootPath + "\\resultfile\\" + result[0], "rb")
        except Exception as e:
            logger.error("报错信息： %s" % e)
        response = FileResponse(final_file)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = "attachment;filename=sql_data.xlsx"
        return response

    @staticmethod
    def options(request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Method'] = request.method
        response['Access-Control-Allow-Origin'] = ['*']
        response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type"
        return response
