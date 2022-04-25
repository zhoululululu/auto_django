# -*- coding: utf-8 -*- 
"""
Created on 2021/7/2 13:43 
@File  : handle_test_case.py
@author: zhoul
@Desc  :
"""
import json
import jsonpath
from auto_django.commonfunc.json_path_finder import JsonPathFinder, get_paths
from auto_django.commonfunc.get_faker import CreatData
from auto_django.commonfunc.get_logging import Logging
from auto_django.commonfunc.datetime_tool import DateTimeTool
from auto_django.commonfunc.yaml_manage import YamlManage
import os
import pandas

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

logging = Logging()


class HandleTestCase(object):
    def __init__(self):
        self.tracking_number_list, self.tracking_number_status_list = [], []
        # self.get_all_tracking_num()

    def handle_special(self, env, key, data=None):
        """
        通过key值，选择不同的处理方式
        :param env:
        :param key:
        :param data:
        :return:
        """
        func_key = key.split("$")[1].split("+")[0]
        func_value = key.split("$")[1].split("+")[1]
        if func_key == "uuid":
            return CreatData.get_uuid(data)
        if func_key.split("+")[0] == "varchar":
            return CreatData.get_varchar(int(func_value))
        if func_key.split("+")[0] == "chinese":
            return CreatData.get_chinese(int(func_value))
        if func_key.split("+")[0] == "num":
            return CreatData.get_num(int(func_value))
        if func_key.split("+")[0] == "strnum":
            return CreatData.get_str_num(int(func_value))
        if func_key in ["punctuation"]:
            return CreatData.get_punctuation(data)
        if func_key == "country":
            return CreatData.get_currency(env, func_value, data)
        if func_key == "trackingNumber":
            # return CreatData.get_tracking_number(env, func_value, data)
            return self.get_tracking_num()
        if func_key == "timeStamp":
            if func_value == "13":
                return DateTimeTool.get_now_time_stamp_with_millisecond()
            elif func_value == "10":
                return DateTimeTool.get_now_time_stamp_with_second()
        if func_key == "orderData":
            return DateTimeTool.get_order_time()
        else:
            return data

    def get_relation_value(self, data, key_list: list, point_list: list):
        result_list, exp_data, sheet_data = [], "", {}
        for sheet in data:
            if sheet != "case_manage":
                sheet_data[sheet] = data.get(sheet).fillna("").to_dict(orient="list")
        logging.info("读取api_manage外的所有sheet内容为： %s" % sheet_data)
        for i in range(len(key_list)):
            sheet_name, field = key_list[i][1:].split(".")
            try:
                exp_data = sheet_data.get(sheet_name).get(point_list[i])[
                    sheet_data.get(sheet_name).get("key").index(field)]
            except Exception as e:
                exp_data.append("")
                self.logging.error("")
            result_list.append(exp_data)
        return result_list

    def get_deal_params(self, env, origin_params):
        if origin_params != "":
            params_list = eval(origin_params)  # 先将str转json
            if "$" in origin_params:  # 如果发现在原先传入的body中含有$
                paths = get_paths(eval(origin_params))  # 获取body所有的路径
                for path in paths:
                    result = params_list
                    for p in path:
                        result = result[p]
                        if p == path[-1] and type(result) not in [int, float, list]:
                            if result is not None:
                                if "$" in result and "+" in result:
                                    handle_result = self.handle_special(env, result, params_list)
                                    if "country" in result:
                                        params_list = handle_result
                                    else:
                                        params_list = self.change_value_test(params_list, p, handle_result)
                # logging.info("params处理成功：%s -> %s" % (str(origin_params), params_list))
        else:
            params_list = origin_params
        return params_list

    @staticmethod
    def update_validation_data(env, data, service):
        """
        针对validation修改sellerISID
        :param service:
        :param data:
        :param env:
        :return:
        """
        params_data = json.loads(data)
        if service == "经济":
            params_data["service"] = "EE"
        elif service == "标准":
            params_data["service"] = "ES"
        elif service == "mini":
            params_data["service"] = "EM"
        elif service == "快捷":
            params_data["service"] = "EX"
        if env == "test":
            params_data["sellerInfo"]["sellerIsId"] = "2220040455552376"
            params_data["sellerInfo"]["sellerMasterId"] = "2220040455552376"
        elif env == "pre":
            params_data["sellerInfo"]["sellerIsId"] = "8795643389440413"
            params_data["sellerInfo"]["sellerMasterId"] = "8795643389440413"
        elif env == "stage":
            params_data["sellerInfo"]["sellerIsId"] = "2835151170368532"
            params_data["sellerInfo"]["sellerMasterId"] = "2835151170368532"
        elif env == "pro":
            params_data["sellerInfo"]["sellerIsId"] = "2580585480128309"
            params_data["sellerInfo"]["sellerMasterId"] = "2580585480128309"
        return params_data

    def change_value_test(self, json_dict, k, v, v_type=None):
        """
        替换json值
        :param json_dict: 需要进行修改的json值
        :param k: 要替换的key
        :param v: 要替换的value
        :param type: 类型，用于区分是不是length
        :return:
        """
        if isinstance(json_dict, list):  # 判断json_dict是否为list
            for j_dict in json_dict:  # 遍历list的值，一一进入
                self.change_value_test(j_dict, k, v, v_type=type(j_dict))  # 继续递归
        elif isinstance(json_dict, dict):  # 判断json_dict是否为dict
            for key in json_dict:  # 遍历
                if key == k:  # 找到
                    if v_type != "length":
                        json_dict[key] = v if v != '""' else ""  # 替换
                    else:
                        json_dict[key] = json_dict[key].split("+")[0] + "+" + str(v)
                elif isinstance(json_dict[key], (dict, list)):  # 或满足dict或json，继续递归遍历
                    self.change_value_test(json_dict[key], k, v, v_type=type(json_dict[key]))
        return json_dict

    def collection_data(self, test_case_id, collection_data, test_data, result):
        """
        收集请求结果参数，写在yaml中，格式为case_id: key, value
        :param test_data:
        :param test_case_id:
        :param collection_data:
        :param result:
        :return:
        """
        ym_writer = YamlManage(rootPath + "\\data\\collection_data.yaml")
        for path in collection_data:
            re = result
            for p in path:
                re = re[p]
                if p == path[-1]:
                    ym_writer.write_yaml(test_case_id, p, re)

    # def get_all_tracking_num(self):
    #     testdata = pandas.read_excel(rootPath + "\\data\\jitu\\jt-order.xlsx", sheet_name="SGtrackingNumber")
    #     self.tracking_number_list = testdata.跟踪号码.tolist()
    #     self.tracking_number_status_list = testdata.状态.tolist()

    # def get_tracking_num(self):
    #     for i in range(len(self.tracking_number_list)):
    #         if "未使用" in self.tracking_number_status_list[i]:
    #             return self.tracking_number_list[i]
    #
    # def update_tracking_num(self, tracking_number):
    #     for i in range(len(self.tracking_number_list)):
    #         if tracking_number == self.tracking_number_list[i]:
    #             self.tracking_number_status_list[i] = "已使用"
    #     result = pandas.DataFrame({"跟踪号码": self.tracking_number_list, "状态": self.tracking_number_status_list})
    #     result.to_excel(rootPath + "\\data\\jitu\\jt-order.xlsx", sheet_name="SGtrackingNumber")

    def get_deal_params_with_desc(self, env, origin_params, desc=None):
        if origin_params != "":
            params_list = json.loads(origin_params)  # 还原json格式的请求data，方便进行后续赋值
            if desc != "":  # 判断是否有desc
                if "value" in desc:  # 判断desc中是否含有value，因为必填参数会有value=''，或者None的情况
                    key = desc.split(".value=")[0]
                    if "." in key:
                        k_list = key.split(".")
                        key = k_list[len(k_list) - 1]
                        k_value = k_list[:len(k_list) - 1]
                        value = params_list
                        for i in k_value:
                            value = value.get(i)
                            if type(value) is list:
                                value = value[0]
                    value = desc.split(".value=")[1] if desc.split(".value=")[1] != "null" else None
                    params_list = self.change_value_test(params_list, key, value, type(params_list))
                elif "length" in desc:  # 判断desc是否含有length，长度有=><三种情况
                    key = desc.split(".length")[0]
                    if "." in key:
                        k_list = key.split(".")
                        key = k_list[len(k_list) - 1]
                        k_value = k_list[:len(k_list) - 1]
                        value = params_list
                        for i in k_value:
                            value = value.get(i)
                            if type(value) is list:
                                value = value[0]
                    for_value = desc.split(".length")[1]  # 选取到value
                    v_type = "varchar"
                    if type(value) is int:
                        v_type = "num"
                    if key in ["consigneePhone", "consigneeZipCode", "sellerPhone",
                               "sellerZipCode"]:
                        v_type = "strnum"
                    if key == "skuDescCn":
                        v_type = "chinese"
                    if "=" in for_value:  # =
                        value = self.handle_special(env, "$" + v_type + "+" + str(int(for_value.split("=")[1])))
                    elif ">" in for_value:  # >
                        value = self.handle_special(env, "$" + v_type + "+" + str(
                            int(for_value.split(">")[1]) + 1))  # 大于时，自动长度+1
                    elif "<" in for_value:  # <
                        value = self.handle_special(env, "$" + v_type + "+" + str(
                            int(for_value.split("<")[1]) - 1))  # 小于时，自动长度-1
                    elif "<=" in for_value or "<=" in for_value:  # <=
                        value = self.handle_special(env, "$" + v_type + "+" + str(
                            int(for_value.split("<=")[1]) - 1))  # 小于时，自动长度-1
                    params_list = self.change_value_test(params_list, key, value, v_type="length")  # 调用函数进行替换
            paths = get_paths(params_list)  # 获取body所有的路径
            for path in paths:
                result = params_list  # 为了后面的赋值临时定义result
                for p in path:
                    result = result[p]
                    if p == path[-1] and type(result) not in [int, float, list]:
                        if result is not None:
                            if "$" in result and "+" in result:
                                handle_result = self.handle_special(env, result, params_list)
                                if "country" in result:
                                    params_list = handle_result
                                else:
                                    params_list = self.change_value_test(params_list, p, handle_result)
                # logging.info("params处理成功：%s -> %s" % (str(origin_params), params_list))
        else:
            params_list = origin_params

        print("\n")
        print(params_list)
        return params_list


if __name__ == '__main__':
    qqq = HandleTestCase()
    final_json_value = {
        'data': {'hoauBagId': 'gRX3aasrWeTmO', 'bagWeight': 100, 'lastMileCountry': 'MY', 'battery': '', 'incoterm': 0,
                 'packageInfoList': [
                     {'trackingNumber': 640827310700, 'consigneeFullName': 'BOUCHRA', 'consigneePhone': '11231234566',
                      'consigneeCountry': 'MY', 'consigneeState': 'Germany', 'consigneeCity': 'Marl',
                      'consigneeDistrict': 'Marl', 'consigneeAddr1': 'Allensteiner Str. 11',
                      'consigneeZipCode': '16150', 'sellerFullName': 'Jackie Chan', 'sellerPhone': '12345678911',
                      'sellerCountry': 'CN', 'sellerState': 'BEIJING', 'sellerCity': 'BEIJING',
                      'sellerDistrict': 'BEIJING', 'sellerAddr1': 'fahuoren dizhiyi', 'sellerZipCode': '123456',
                      'lastMileServiceCode': 'JTMYSTD', 'packageTotalValue': 6.91, 'currency': 'USD',
                      'packageTotalWeight': 2000.0, 'battery': '', 'incoterm': 0, 'itemInfoList': [
                         {'skuDesc': 'CCEI-Test3', 'skuDescCn': 'CCEI-Test3', 'skuValue': 6.91, 'currency': 'USD'}]}]}}

    qqq.update_tracking_num(
        final_json_value["data"]["packageInfoList"][0][
            "trackingNumber"])
#     test = '{"data":{"project":"eBay","hoauBagId":"$varchar+13","bagWeight":100,"mawb":"526-58571376","lineHaulVendorName":"MC","lineHaulCountry":"CN","lineHaulGateWay":"HKG","lineHaulServiceCode":"FAST","lastMileCountry":"NL","lastMileGateWay":"AMS","lastMileLocation":"SP-AMS","lastMileServiceCode":"IMX","lastMileVendorName":"SP","battery":0,"incoterm":0,"lengthUnit":0,"weightUnit":0,"packageInfoList":[{"trackingNumber":"$varchar+13","consigneeFullName":"BOUCHRA","consigneePhone":"11231234566","consigneeCountry":"NL","consigneeState":"Germany","consigneeCity":"Marl","consigneeDistrict":"Marl","consigneeAddr1":"Allensteiner Str. 11","consigneeZipCode":"45770","sellerFullName":"Jackie Chan","sellerPhone":"12345678911","sellerCountry":"CN","sellerState":"BEIJING","sellerCity":"BEIJING","sellerDistrict":"BEIJING","sellerAddr1":"fahuoren dizhiyi","sellerZipCode":"123456","lastMileServiceCode":"IMX","packageHeight":6.91,"packageLength":6.91,"packageTotalValue":6.91,"currency":"EUR","packageTotalWeight":2000.00,"packageWidth":5.00,"battery":0,"incoterm":0,"itemInfoList":[{"sku":"1611553510699","skuDesc":"CCEI-Test3","skuDescCn":"CCEI-Test3","skuValue":6.91,"currency":"EUR","quantity":1,"skuWeight":10.00,"hscode":"010000","link":"www.ebay.com"}]}]}}'
#     print(
#         qqq.get_deal_params_with_desc("test", test, 'data.hoauBagId.value=null'),
#         "dict")
#     print(
#         qqq.get_deal_params_with_desc("test", test, 'data.packageInfoList.itemInfoList.sku.value=null'),
#         "dict")
#     print(
#         qqq.get_deal_params_with_desc("test", test, 'data.packageInfoList.packageHeight.value=null'),
#         "dict")
#     print(
#         qqq.get_deal_params_with_desc("test", test, 'data.packageInfoList.itemInfoList.skuDesc.value=null'),
#         "dict")
#     print(
#         qqq.get_deal_params_with_desc("test", test, 'data.packageInfoList.itemInfoList.skuDesc.length=31'),
#         "dict")
