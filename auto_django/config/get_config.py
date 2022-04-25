# -*- coding: UTF-8 -*-
"""
Created on 2020/2/29
@File  : get_config.py
@author: zhoul
@Desc  :
"""

import os
from auto_django.commonfunc.file_manage import FileManage
from auto_django.commonfunc.yaml_manage import YamlManage

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Config(object):
    def __init__(self, type):
        """
        初始化config，读取config文件
        """
        if type == "order":
            self.file_path = rootPath + "\\config\\sorting_consignee.xlsx"
            self.config = FileManage.file_to_dict(self.file_path, "sorting_consignee")
        else:
            if type == "email":
                self.file_path = rootPath + "\\config\\config.yaml"
            elif type == "url":
                self.file_path = rootPath + "\\config\\http_config.yaml"
            elif type == "sql":
                self.file_path = rootPath + "\\config\\mysql_config.yaml"
            elif type == "json":
                self.file_path = rootPath + "\\config\\json.yaml"
            self.config = YamlManage(self.file_path)
            self.conf = {}

    def get_email_info(self):
        """
        获取email的各种参数配置值
        """
        self.conf['service'] = self.config.read_yaml(self.file_path, "Email", "service")
        self.conf['version'] = self.config.read_yaml(self.file_path, "Email", "version")
        self.conf['tester'] = self.config.read_yaml(self.file_path, "Email", "tester")
        self.conf['remark'] = self.config.read_yaml(self.file_path, "Email", "remark")
        self.conf['is_send'] = self.config.read_yaml(self.file_path, "Email", "is_send")
        self.conf['user'] = self.config.read_yaml(self.file_path, "Email", "user")
        self.conf['password'] = self.config.read_yaml(self.file_path, "Email", "password")
        self.conf['host'] = self.config.read_yaml(self.file_path, "Email", "host")
        self.conf['rec_users'] = self.config.read_yaml(self.file_path, "Email", "rec_users")
        self.conf['title'] = self.config.read_yaml(self.file_path, "Email", "title")
        return self.conf

    def get_sql_info(self, env, sortation="dg"):
        """
        获取mql数据库的各种参数配置值
        :param sortation:
        :param env:the env which you choose
        :return:
        """
        if env in ["test", "pre", "stage"]:
            self.conf["sys_user"] = self.config.read_yaml("author")
            self.conf['url'] = self.config.read_yaml(env, "url")
            self.conf['collection_type'] = self.config.read_yaml(env, [sortation, "collection_type"])
            self.conf['drop_id'] = self.config.read_yaml(env, [sortation, "drop_id"])
            self.conf['is_id'] = self.config.read_yaml(env, "isId")
            self.conf['seller_addr_id'] = self.config.read_yaml(env, "seller_addr_id")
        elif env in ["pro_oc"]:
            self.conf["ssh_host"] = self.config.read_yaml(env, "ssh_host")
            self.conf['ssh_port'] = self.config.read_yaml(env, "ssh_port")
            self.conf['ssh_user'] = self.config.read_yaml(env, "ssh_user")
            self.conf['ssh_password'] = self.config.read_yaml(env, "ssh_password")
        else:
            self.conf["sys_user"], self.conf['url'], self.conf['collection_type'], self.conf['drop_id'], self.conf[
                'is_id'], self.conf['seller_addr_id'], self.conf['validation'] = "", "", "", "", "", "", ""
        self.conf['db_host'] = self.config.read_yaml(env, "host")
        self.conf['db_port'] = self.config.read_yaml(env, "port")
        self.conf['user_name'] = self.config.read_yaml(env, "user")
        self.conf['user_pwd'] = self.config.read_yaml(env, "password")
        self.conf['db'] = self.config.read_yaml(env, "database")
        return self.conf

    def get_json_value(self, country):
        """
        获取order-flow相关的
        :param country:国家
        :return:
        """
        self.conf['ship_order'] = self.config.read_yaml("ship_order")
        self.conf['get_letter_dg'] = self.config.read_yaml("get_letter_dg")
        self.conf['get_letter_not_dg'] = self.config.read_yaml("get_letter_not_dg")
        self.conf['get_label_dg'] = self.config.read_yaml("get_label_dg")
        self.conf['get_label_not_dg'] = self.config.read_yaml("get_label_not_dg")
        self.conf['bu_bag'] = self.config.read_yaml("bu_bag")
        self.conf['get_last_mile_bag'] = self.config.read_yaml("get_last_mile_bag")
        self.conf['bag_weight'] = self.config.read_yaml("bag_weight")
        self.conf['out_package'] = self.config.read_yaml("out_package")
        self.conf['consignee_full_name'] = self.config.read_yaml("consignee", [country, "consigneeFullName"])
        self.conf['consignee_phone'] = self.config.read_yaml("consignee", [country, "consigneePhone"])
        self.conf['consignee_state'] = self.config.read_yaml("consignee", [country, "consigneeState"])
        self.conf['consignee_city'] = self.config.read_yaml("consignee", [country, "consigneeCity"])
        self.conf['consignee_zip_code'] = self.config.read_yaml("consignee", [country, "consigneeZipCode"])
        self.conf['address'] = self.config.read_yaml("consignee", [country, "address"])
        self.conf['address2'] = self.config.read_yaml("consignee", [country, "address2"])
        self.conf['sku_desc_cn'] = self.config.read_yaml("consignee", [country, "skuDescCn"])
        self.conf['sku_desc'] = self.config.read_yaml("consignee", [country, "skuDesc"])
        return self.conf

    def get_urls(self, env, sortation):
        self.conf['validation_url'] = self.config.read_yaml(sortation + "_" + env, "validation_url")
        self.conf['ship_order'] = self.config.read_yaml(sortation + "_" + env, "ship_order")
        self.conf['sortation_code'] = self.config.read_yaml(sortation + "_" + env, "sort_code")
        self.conf['drop_site_id'] = self.config.read_yaml(sortation + "_" + env, "drop_site_id")
        self.conf['drop_site_id'] = self.config.read_yaml(sortation + "_" + env, "drop_site_id")
        self.conf['get_letter'] = self.config.read_yaml(sortation + "_" + env, "get_letter")
        self.conf['get_label'] = self.config.read_yaml(sortation + "_" + env, "get_label")
        self.conf['bu_bag'] = self.config.read_yaml(sortation + "_" + env, "bu_bag")
        self.conf['get_last_mile_bag'] = self.config.read_yaml(sortation + "_" + env, "get_last_mile_bag")
        self.conf['bag_weight'] = self.config.read_yaml(sortation + "_" + env, "bag_weight")
        self.conf['out_package'] = self.config.read_yaml(sortation + "_" + env, "out_package")
        self.conf['username'] = self.config.read_yaml(sortation + "_" + env, "username")
        self.conf['password'] = self.config.read_yaml(sortation + "_" + env, "password")
        self.conf['pre_label'] = self.config.read_yaml(sortation + "_" + env, "pre_label")
        self.conf['again_label'] = self.config.read_yaml(sortation + "_" + env, "again_label")
        self.conf['login_path'] = self.config.read_yaml(sortation + "_" + env, "login_path")

        return self.conf

    def get_sorting_value(self, country, product, vendor_code, service_code, first_sorting,
                          sorting_result):
        vendor_code_list = self.config["vendorCode"].tolist()
        service_code_list = self.config["serviceCode"].tolist()
        product_list = self.config["product"].tolist()
        first_sorting_list = self.config["firstSorting"].tolist()
        sorting_result_list = self.config["sortingResult"].tolist()
        consignee_full_name_list = self.config["consigneeFullName"].tolist()
        consignee_phone_list = self.config["consigneePhone"].tolist()
        consignee_country_list = self.config["consigneeCountry"].tolist()
        consignee_state_list = self.config["consigneeState"].tolist()
        consignee_city_list = self.config["consigneeCity"].tolist()
        consignee_zipcode_list = self.config["consigneeZipcode"].tolist()
        consignee_address1_list = self.config["consigneeAddress1"].tolist()
        consignee_address2_list = self.config["consigneeAddress2"].tolist()
        sku_value_list = self.config["skuValue"].tolist()
        txn_value_list = self.config["txnValue"].tolist()
        sku_desc_list = self.config["skuDesc"].tolist()
        sku_desc_cn_list = self.config["skuDescCN"].tolist()
        weight_list = self.config["weight"].tolist()
        battery_type_list = self.config["batteryType"].tolist()
        letter_list = self.config["letter"].tolist()
        flag = False
        index_list = [i for i, x in enumerate(vendor_code_list)]
        if country in consignee_country_list:
            country_index = [i for i, x in enumerate(consignee_country_list) if x == country]
            index_list = list(set(index_list) & set(
                country_index))
            flag = True
        if product is not None:
            product_index = [i for i, x in enumerate(product_list) if x == product]
            index_list = list(set(index_list) & set(
                product_index))
            flag = True
        if vendor_code is not None:
            vendor_index = [i for i, x in enumerate(vendor_code_list) if x == vendor_code]
            index_list = list(set(index_list) & set(
                vendor_index))
            flag = True
        if service_code is not None:
            service_index = [i for i, x in enumerate(service_code_list) if x == service_code]
            index_list = list(set(index_list) & set(
                service_index))
            flag = True
        if first_sorting is not None:
            first_sorting_index = [i for i, x in enumerate(first_sorting_list) if x == first_sorting]
            index_list = list(set(index_list) & set(
                first_sorting_index))
            flag = True
        if sorting_result is not None:
            sorting_result_index = [i for i, x in enumerate(sorting_result_list) if x == sorting_result]
            index_list = list(set(index_list) & set(
                sorting_result_index))
            flag = True
        if flag is True:
            first_index = index_list[0]
            result = {"consigneeFullName": consignee_full_name_list[first_index],
                      "consigneeCountry": consignee_country_list[first_index],
                      "consigneeState": consignee_state_list[first_index],
                      "consigneeCity": consignee_city_list[first_index],
                      "consigneePhone": consignee_phone_list[first_index],
                      "consigneeZipcode": consignee_zipcode_list[first_index],
                      "consigneeAddress1": consignee_address1_list[first_index],
                      "consigneeAddress2": consignee_address2_list[first_index],
                      "skuValue": sku_value_list[first_index],
                      "txnValue": txn_value_list[first_index],
                      "weight": weight_list[first_index],
                      "skuDesc": sku_desc_list[first_index],
                      "skuDescCN": sku_desc_cn_list[first_index],
                      "batteryType": battery_type_list[first_index],
                      "letter": letter_list[first_index]}
            return result
        else:
            return "空空如也！"

#
# if __name__ == '__main__':
#     demo = Config("order")
#     print(demo.get_sorting_value(country="AT", vendor_code="SP", product="ES", first_sorting=2, service_code=None,
#                                  sorting_result=None))
