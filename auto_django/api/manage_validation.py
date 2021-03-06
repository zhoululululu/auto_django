# -*- coding: utf-8 -*- 
"""
Created on 2022/1/4 11:07 
@File  : manage_validation.py
@author: zhoul
@Desc  :
"""

from auto_django.commonfunc.handle_test_case import HandleTestCase
from auto_django.commonfunc.assert_tool import AssertTool
from auto_django.commonfunc.request_client import RequestClient
import json
from auto_django.commonfunc.beauty_excel import beauty_format
from rest_framework.views import APIView
from auto_django.commonfunc.get_logging import Logging
from django.http import FileResponse, HttpResponse
from auto_django.commonfunc.datetime_tool import DateTimeTool
from auto_django.models import TValidationTestCase, TValidationResult, TUrlManage
import pandas
import os
from auto_django.commonfunc.wx_robot import WeChat

logger = Logging()

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class NewValidation(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        handle = HandleTestCase()
        env = json.loads(request.body).get("env")
        robot = json.loads(request.body).get("robot")
        if env:
            for i in TUrlManage.objects.filter(name="validation", env=env):
                url_info = i.to_dict()
            url, path, port = url_info.get("url"), url_info.get("path"), url_info.get("port")
            req = RequestClient(url)
            error_des_list, error_data_list, error_res_list, error_assert_list, error_exp_list, error_act_list, error_service_list, error_file_list = [], [], [], [], [], [], [], []
            test_case, all_des_list, all_data_list, all_res_list, all_assert_list, all_exp_list, all_act_list, all_service_list, all_file_list = [], [], [], [], [], [], [], [], []
            all_num, error_num, success_num, skip_num = 0, 0, 0, 0
            headers = {"Content-Type": "application/json"}
            result = {"data": [], "page_total": 0}
            try:
                validation_test_case = TValidationTestCase.objects.filter(is_active=1).order_by(
                    "-create_time")
                for tracking_info in validation_test_case:
                    test_case.append(tracking_info.to_dict())
            except Exception as e:
                logger.error("????????????????????? %s" % e)
                result["data"] = {"error": "????????????"}
            for i in test_case:
                description, product_service, exp_data, check_data, request_data = i.get("desc"), i.get(
                    "service"), i.get(
                    "check_data"), i.get("check_type"), i.get("request_data")
                # print(request_data)
                json_value = handle.update_validation_data(env, request_data, product_service)
                single_result = req.get_request(path, port if port is not None else "", "post", headers=headers,
                                                json_value=json_value,
                                                file_key="", file_value="", timeout=5000)
                assert_result, exp_value, act_value = AssertTool().compare_dict(single_result, exp_data, "", check_data)
                exp_1 = "??????" + product_service + "??????" if exp_value[0][0] is True else "?????????" + product_service + "??????"
                all_data_list.append(str(json_value).replace("'", '"'))
                all_service_list.append(product_service)
                all_des_list.append(description + "-" + product_service)
                all_file_list.append(description)
                all_res_list.append(str(single_result).replace("'", '"'))
                all_exp_list.append(exp_1)
                all_assert_list.append(assert_result)
                if assert_result is False:
                    # ??????????????????
                    error_data_list.append(str(json_value).replace("'", '"'))
                    error_service_list.append(product_service)
                    error_des_list.append(description + "-" + product_service)
                    error_file_list.append(description)
                    error_res_list.append(str(single_result).replace("'", '"'))
                    error_exp_list.append(exp_1)
                    error_assert_list.append(assert_result)
                    error_num += 1
                else:
                    success_num += 1
            all_data_result = pandas.DataFrame(
                {"??????": all_file_list, "????????????": all_service_list, "??????": all_exp_list,
                 "??????????????????": all_assert_list,
                 "????????????": all_data_list,
                 "????????????": all_res_list})
            data_result = pandas.DataFrame(
                {"??????": error_file_list, "????????????": error_service_list, "??????": error_exp_list,
                 "??????????????????": error_assert_list,
                 "????????????": error_data_list,
                 "????????????": error_res_list})
            error_file = DateTimeTool.get_now_date() + "_" + env + "_validation_result.xlsx"
            writer = pandas.ExcelWriter(rootPath + "\\resultfile\\validation\\" + error_file)
            all_data_result.to_excel(writer, sheet_name="??????????????????")
            data_result.to_excel(writer, sheet_name="????????????")
            writer.save()
            beauty_format(rootPath + "\\resultfile\\validation\\" + error_file)

            TValidationResult.objects.create(env=env, test_case_num=len(all_data_list),
                                             success_num=len(all_data_list) - len(error_des_list),
                                             failed_num=len(error_des_list), pass_rate="{:.2%}".format(
                    (len(all_des_list) - len(error_des_list)) / len(all_des_list)),
                                             result="??????" if len(error_des_list) == 0 else "??????",
                                             result_file_name=error_file,
                                             create_user="Test", create_time=DateTimeTool.get_now_time(), is_active=1)
            result["data"] = {"success": "true"}
            data = {
                "msgtype": "markdown",  # ??????????????????????????????markdown
                "markdown": {
                    "content": "# **<%s>-??????????????????**\n#### **????????????????????????**\n"
                               "> ???????????????<font color=\"info\">%s</font> \n"
                               "> ?????????????????????<font color=\"info\">%s???</font>???????????????????????????<font color=\"info\">%s</font>\n"
                               "> **--------------------????????????--------------------**\n"
                               "> **????????????**<font color=\"info\">%s</font>\n**????????????**<font color=\"red\">%s</font>\n" % (
                                   env, "validation", len(all_des_list), "{:.2%}""".format(
                                       (len(all_des_list) - len(error_des_list)) / len(all_des_list)),
                                   (len(all_des_list) - len(error_des_list)), len(error_des_list))}}
            data[
                "markdown"][
                "content"] += "> **--------------------????????????--------------------**\n" if len(
                error_des_list) != 0 else "> **--------------------????????????--------------------**\n"
            for i in error_des_list:
                error_record = "> **?????????**<font color=\"warning\">%s</font>\n" % i
                data["markdown"]["content"] += error_record
            data["markdown"]["content"] += "> ##### **????????????????????????????????????**"
            if robot:
                path1 = "/cgi-bin/webhook/send?key=%s" % robot
                path2 = "/cgi-bin/webhook/upload_media?key=%s&type=file" % robot
                lulu_robot = WeChat(path1, path2)
                lulu_robot.send_message(data)
                lulu_robot.send_file(rootPath + "\\resultfile\\validation\\" + error_file)
        else:
            result = {"statusCode": 10000, "error": "env????????????"}
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


class DeleteValidation(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        result = {"statusCode": 0, "message": "validation????????????????????????"}
        try:
            if "," not in str(id):
                TValidationResult.objects.filter(id=id).update(is_active=0)
            else:
                id_list = id.split(",")
                for i in id_list:
                    TValidationResult.objects.filter(id=i).update(is_active=0)
        except Exception as e:
            logger.error("????????????????????? %s" % e)
            result = {"statusCode": 10000, "error": "validation????????????????????????"}
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


class DownloadValidation(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        id = json.loads(request.body).get("id")
        try:
            t_result = TValidationResult.objects.filter(id=id)[0]
            result_file_name = t_result.to_dict().get("result_file_name")
            file = open(rootPath + "\\resultfile\\validation\\" + result_file_name, "rb")
        except Exception as e:
            logger.error("??????????????? %s" % e)
        response = FileResponse(file)
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


class QueryValidation(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        page_index = json.loads(request.body).get("page_index")
        page_size = json.loads(request.body).get("page_size")
        env = json.loads(request.body).get("env")
        result = {"list": []}
        try:
            if env:
                sql_result = TValidationResult.objects.filter(env=env, is_active=1).order_by(
                    "-create_time")
            else:
                sql_result = TValidationResult.objects.filter(is_active=1).order_by(
                    "-create_time")
            for check_result_info in sql_result[(page_index - 1) * page_size:page_index * page_size]:
                result["list"].append(check_result_info.to_dict())
            result["page_total"] = len(sql_result)
        except Exception as e:
            logger.error("????????????????????? %s" % e)
            result = {"statusCode": 10000, "message": "??????validation??????????????????"}
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
