# -*- coding: utf-8 -*- 
"""
Created on 2021/7/8 13:35 
@File  : config_json_value.py
@author: zhoul
@Desc  :
"""
from config.get_config import Config
from sql.sql_statement import OCSqlStatement, RDCSqlStatement, TaurusSqlStatement
from commonfunc.datetime_tool import DateTimeTool
import json
from case.generate_tracking_number import GenerateTrackingNumber


class ConfigJsonValue(object):

    def __init__(self, env, sortation, service_id, country, battery, tracking_num, vendor_code=None, service_code=None,
                 first_sorting=None,
                 sorting_result=None):
        """
        初始化
        :param env: 环境
        :param service_id: 订单的服务：ES标准，EE经济等等
        :param config_type: 读取yaml的参数：json为读取json参数
        """
        self.env = env
        self.sortation = sortation
        self.service_id = service_id
        self.country = country
        self.battery = battery
        self.config = Config("json").get_json_value(country)  # 获取特定国家对应的收件人信息
        self.order_config = Config("order").get_sorting_value(country, service_id, vendor_code, service_code,
                                                              first_sorting, sorting_result)
        self.url_config = Config("url").get_urls(env, sortation)
        self.sql_config = Config("sql").get_sql_info(env, sortation)
        self.oc_cursor = OCSqlStatement(env)
        self.rdc_cursor = RDCSqlStatement(sortation, env)
        self.ts_cursor = TaurusSqlStatement(self.env)
        self.tracking_number = GenerateTrackingNumber().generate_tracking_num(self.env, self.service_id)[
            0] if tracking_num == "" else tracking_num

    def get_ship_order_data(self, package_total_weight, sku_value, consignee_full_name, consignee_phone,
                            consignee_state, consignee_city,
                            consignee_zipcode, consignee_address1, consignee_address2, txn_value, sku_desc,
                            sku_desc_cn,
                            battery_type,
                            ele_id, letter):
        """
        封装IS下单参数
        :param letter:
        :param consignee_phone:
        :param ele_id:
        :param battery_type:
        :param sku_desc_cn:
        :param sku_desc:
        :param txn_value:
        :param consignee_address2:
        :param consignee_address1:
        :param consignee_zipcode:
        :param consignee_city:
        :param consignee_state:
        :param consignee_full_name:
        :param package_total_weight: 包裹重量
        :param sku_value: 申报价格
        :return: 下单参数
        """
        currency = self.ts_cursor.taurus_code(self.country)  # 获取国家的货币
        # 对下单参数进行封装操作
        final_ship_order_data = eval(
            self.config["ship_order"] % (
                self.sql_config["is_id"], self.sql_config["is_id"], self.url_config["drop_site_id"],
                self.sql_config["seller_addr_id"],
                self.config["consignee_full_name"] if consignee_full_name is None else consignee_full_name,
                self.config["consignee_phone"] if consignee_phone is None else consignee_phone,
                self.country, self.config["consignee_state"] if consignee_state is None else consignee_state,
                self.config["consignee_city"] if consignee_city is None else consignee_city,
                self.config["address"] if consignee_address1 is None else consignee_address1,
                self.config["address2"] if consignee_address2 is None else consignee_address2,
                self.config["consignee_zip_code"] if consignee_zipcode is None else consignee_zipcode,
                self.tracking_number, self.service_id, package_total_weight, currency,
                self.config["sku_desc_cn"] if sku_desc_cn is None else sku_desc_cn,
                self.config["sku_desc"] if sku_desc is None else sku_desc, sku_value, currency,
                sku_value if txn_value is None else txn_value,
                self.config["sku_desc"] if sku_desc is None else sku_desc,
                self.config["sku_desc_cn"] if sku_desc_cn is None else sku_desc_cn))
        # 额外操作: 如果带电的话，目前暂不支持多商品
        if battery_type != "0":
            if self.env == "test":
                final_ship_order_data["data"]["isId"] = "2220040455552376"
                final_ship_order_data["data"]["isMasterId"] = "2220040455552376"
                # 内置锂离子电池
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "batteryType"] = "PI967SEC2" if battery_type == "1" else battery_type
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "elecQuaID"] = "8375691546944" if ele_id is None else ele_id
                # 配套锂电池
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                #     "batteryType"] = "PI969SEC2" if battery_type is None else battery_type
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                #     "elecQuaID"] = "8375046178176" if ele_id is None else ele_id
            elif self.env == "pre":
                # 内置锂金属电池
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "batteryType"] = "PI970SEC2" if battery_type == "1" else battery_type
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "elecQuaID"] = "9585096560360" if ele_id is None else ele_id
                # 内置锂离子电池
                # final_ship_order_data["data"]["isMasterId"] ="2579478844736488"
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                #     "batteryType"] = "PI967SEC2" if battery_type is None else battery_type
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                #     "elecQuaID"] = "4598958935556" if ele_id is None else ele_id
            elif self.env == "stage":
                # 锂金属电池
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "batteryType"] = "PI970SEC2" if battery_type == "1" else battery_type
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "elecQuaID"] = "8462806066756" if ele_id is None else ele_id
        return self.tracking_number, final_ship_order_data, package_total_weight, letter

    def get_ship_order_data_with_sorting(self):
        """
        封装IS下单参数
        :return: 下单参数
        """
        currency = self.ts_cursor.taurus_code(self.country)  # 获取国家的货币
        letter_statue = self.order_config.get("letter")
        # 对下单参数进行封装操作
        final_ship_order_data = eval(
            self.config["ship_order"] % (
                self.sql_config["is_id"], self.sql_config["is_id"], self.url_config["drop_site_id"],
                self.sql_config["seller_addr_id"], self.order_config.get("consigneeFullName"),
                self.order_config.get("consigneePhone"),
                self.country, self.order_config.get("consigneeState"),
                self.order_config.get("consigneeCity"), self.order_config.get("consigneeAddress1"),
                self.order_config.get("consigneeAddress2"),
                self.order_config.get("consigneeZipcode"),
                self.tracking_number, self.service_id, self.order_config.get("weight"), currency,
                self.order_config.get("skuDescCN"), self.order_config.get("skuDesc"), self.order_config.get("skuValue"),
                currency,
                self.order_config.get("txnValue"), self.order_config.get("skuDesc"),
                self.order_config.get("skuDescCN")))
        battery_type = self.order_config.get("batteryType")
        # 额外操作: 如果带电的话，目前暂不支持多商品
        if battery_type != 0:
            if self.env == "test":
                final_ship_order_data["data"]["isId"] = "2220040455552376"
                final_ship_order_data["data"]["isMasterId"] = "2220040455552376"
                # 内置锂离子电池
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["batteryType"] = "PI967SEC2"
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["elecQuaID"] = "8375691546944"
                # 配套锂电池
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["batteryType"] = "PI969SEC2"
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["elecQuaID"] = "8375046178176"
            elif self.env == "pre":
                # 内置锂金属电池
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["batteryType"] = "PI970SEC2"
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "elecQuaID"] = "9585096560360"
                # 内置锂离子电池
                # final_ship_order_data["data"]["isMasterId"] ="2579478844736488"
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["batteryType"] = "PI967SEC2"
                # final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                #     "elecQuaID"] = "4598958935556"
            elif self.env == "stage":
                # 锂金属电池
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["batteryType"] = "PI970SEC2"
                final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0][
                    "elecQuaID"] = "8462806066756"
        return self.tracking_number, final_ship_order_data, self.order_config.get("weight"), battery_type, letter_statue

    def get_b_post_data(self, sortation_code):
        """
        封装比邮大包号接口参数
        :param sortation_code: 分拣中心
        :return: 下单参数
        """
        b_post_data = eval(
            self.config["get_last_mile_bag"] % (
                sortation_code, DateTimeTool.get_now_time(), DateTimeTool.get_now_time()))

        return b_post_data

    def get_letter_data(self, sortation_code):
        """
        封装打标接口参数
        :param sortation_code: 分拣中心
        :return: 下单参数
        """
        # 二话不说,先判断分拣中心是东莞还是非东莞,封装letter_data,因为入参有略微不同
        letter_data = eval(
            self.config["get_letter_dg"] % (
                sortation_code, self.tracking_number, DateTimeTool.get_now_time())) if sortation_code == "05" else eval(
            self.config["get_letter_not_dg"] % (sortation_code, self.tracking_number, DateTimeTool.get_now_time(),
                                                DateTimeTool.get_now_time()))
        return self.tracking_number, letter_data

    def get_label_data(self, sortation_code, package_weight):
        """
        封装分拣换单接口参数
        :param sortation_code: 分拣中心
        :param package_weight: 包裹重量
        :return: 下单参数
        """
        # 同样二话不说,先判断分拣中心是东莞还是非东莞,封装label_data,因为入参有略微不同
        label_data = eval(
            self.config["get_label_dg"] % (
                DateTimeTool.get_now_time(), package_weight, self.tracking_number)) if sortation_code == "05" else eval(
            self.config["get_label_not_dg"] % (
                DateTimeTool.get_now_time(), package_weight, self.tracking_number, sortation_code,
                DateTimeTool.get_now_time()))
        return self.tracking_number, label_data

    def get_bu_bag_data(self, sortation_code, bag_real_weight, first_sorting_result, sorting_result,
                        last_mile_tracking_number):
        """
        封装分拣换单接口参数，不过暂时不做多小包结包，后期在优化吧
        :param sortation_code: 分拣中心
        :param bag_real_weight: 包裹重量
        :param first_sorting_result: 初分垛口
        :param sorting_result: 细分垛口
        :param last_mile_tracking_number: 尾程面单号
        :return: 下单参数
        """
        # 先封装参数
        status = ""
        bu_bag_data = eval(
            self.config["bu_bag"] % (
                sortation_code, bag_real_weight, self.battery, first_sorting_result, sorting_result,
                DateTimeTool.get_now_time(), last_mile_tracking_number, DateTimeTool.get_now_time()))
        # 如果是美国且是嘉兴仓的订单，需要加入mawb参数
        if self.country == "US" and sortation_code == "08":
            bu_bag_data["data"]["mawb"] = self.rdc_cursor.get_mawb(sorting_result)
        last_mile_bag_id = self.rdc_cursor.select_bpost(sorting_result)
        if last_mile_bag_id in ("UBIEUSEMI"):
            status = "b_post"
            print("比邮大包,需要走比邮建包流程...")
        elif last_mile_bag_id in ("UBICASEMI"):
            status = "k_post"
            print("皇邮大包,需要走皇邮建包流程...")
        return bu_bag_data, status

    def get_bag_weight_data(self, bag_real_weight, bag_id):
        """
        封装负重接口参数
        :param bag_real_weight: 包裹重量
        :param bag_id: 大包号
        :return: 负重接口参数
        """
        bag_weight_data = eval(self.config["bag_weight"] % (bag_real_weight, bag_id, DateTimeTool.get_now_time()))
        return bag_weight_data

    def get_out_package_data(self, bag_id):
        """
        封装出库接口参数
        :param bag_id: 大包号
        :return: 负重接口参数
        """
        out_package_data = eval(
            self.config["out_package"] % (
                bag_id, DateTimeTool.get_now_time(), DateTimeTool.get_now_time_stamp_with_second(),
                DateTimeTool.get_now_time(), DateTimeTool.get_how_days_after(1), DateTimeTool.get_now_time()))
        return out_package_data

#
# if __name__ == '__main__':
#     # env, sortation, service_id, country, battery, config_type="json"
#     #     # ConfigJsonValue("test", "ES", "GB").get_letter_data("05")
#     #     ConfigJsonValue("test", "ES", "GB", "1").get_out_package_data("07")
#     # ConfigJsonValue("test", "ES", "US", "1").get_bu_bag_data("08", "100", "1", "51")
#     # ConfigJsonValue("test", "ES", "GB").get_label_data("08", "500")
#     ConfigJsonValue("test", 'dg', "ES", 'DE', '1').get_ship_order_data(100, 1)
