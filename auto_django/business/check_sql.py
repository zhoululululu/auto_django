# -*- coding: utf-8 -*- 
"""
Created on 2021/8/20 9:49 
@File  : check_sql.py
@author: zhoul
@Desc  :
"""

from auto_django.commonfunc.db_client import MysqlClient
from auto_django.commonfunc.file_manage import FileManage
import os
from auto_django.sql.check_sql_statement import CheckSqlStatement

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class CheckSql(object):

    def __init__(self, file):
        # 读取Excel文件中的sheet_name为trackingNumber的trackingNumber列数据
        self.tracking_number_data_list = []
        self.mawb_list = []
        tracking_number = FileManage.file_to_dict(file, sheet_name="trackingNumber").get("trackingNumber").tolist()
        self.control_len(tracking_number)
        for i in tracking_number:
            self.tracking_number_data_list.append(str(i).strip())
        self.tracking_number_data = tuple(self.tracking_number_data_list)
        # 读取Excel文件中的sheet_name为mawb的mawb列数据
        mawb = FileManage.file_to_dict(file, sheet_name="mawb").get("mawb").tolist()
        self.control_len(mawb)
        for i in mawb:
            self.mawb_list.append(str(i).strip())
        self.data_len = len(self.tracking_number_data_list) + len(self.mawb_list)  # 测试数据量
        self.mawb_data = tuple(self.mawb_list[:len(self.mawb_list)])
        self.aq_status, self.rdc_statues, self.error_table, self.final_result = "", "", [], {}

    def control_len(self, test_list):
        if len(test_list) == 1:
            return test_list.append("")
        else:
            return test_list

    def check_aq(self):
        self.oc_cursor = MysqlClient("pro_oc")  # oc数据库游标
        # aquarius.t_waybill
        self.error_table = CheckSqlStatement.check_t_waybill(self.oc_cursor, self.tracking_number_data,
                                                             self.error_table)
        # aquarius.t_waybill_product
        self.error_table = CheckSqlStatement.check_t_waybill_product(self.oc_cursor, self.tracking_number_data,
                                                                     self.error_table)
        # aquarius.t_waybill_process_expected
        self.error_table = CheckSqlStatement.check_t_waybill_process_expected(self.oc_cursor,
                                                                              self.tracking_number_data,
                                                                              self.error_table)
        # aquarius.t_waybill_pickup
        self.error_table = CheckSqlStatement.check_t_waybill_pickup(self.oc_cursor,
                                                                    self.tracking_number_data,
                                                                    self.error_table)
        # aquarius.t_waybill_consignee
        self.error_table = CheckSqlStatement.check_t_waybill_consignee(self.oc_cursor,
                                                                       self.tracking_number_data,
                                                                       self.error_table)
        # aquarius.t_waybill_sorting
        self.error_table = CheckSqlStatement.check_t_waybill_sorting(self.oc_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        # aquarius.t_waybill_combine
        self.error_table = CheckSqlStatement.check_t_waybill_combine(self.oc_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        # aquarius.t_acas_inspect_bag_detail
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag_detail(self.oc_cursor,
                                                                             self.tracking_number_data, self.mawb_data,
                                                                             self.error_table)
        # aquarius.t_acas_inspect_bag
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag(self.oc_cursor, self.mawb_data,
                                                                      self.error_table)
        # aquarius.t_bag_sortation_out_combine_detail
        self.error_table = CheckSqlStatement.check_t_bag_sortation_out_combine_detail(self.oc_cursor,
                                                                                      self.tracking_number_data,
                                                                                      self.error_table)
        # aquarius.t_bag_sortation_out_combine
        self.error_table = CheckSqlStatement.check_t_bag_sortation_out_combine(self.oc_cursor,
                                                                               self.tracking_number_data,
                                                                               self.error_table)
        # aquarius.t_waybill_sorting_combine
        self.error_table = CheckSqlStatement.check_t_waybill_sorting_combine(self.oc_cursor,
                                                                             self.tracking_number_data,
                                                                             self.error_table)
        # aquarius.t_bag_vendor_dhl
        self.error_table = CheckSqlStatement.check_t_bag_vendor_dhl(self.oc_cursor,
                                                                    self.tracking_number_data,
                                                                    self.error_table)
        # aquarius.t_bag_vendor_detail_dhl
        self.error_table = CheckSqlStatement.check_t_bag_vendor_detail_dhl(self.oc_cursor,
                                                                           self.tracking_number_data,
                                                                           self.error_table)
        # aquarius.t_bag_sortation_out
        self.error_table = CheckSqlStatement.check_t_bag_sortation_out(self.oc_cursor,
                                                                       self.tracking_number_data,
                                                                       self.error_table)
        # aquarius.t_bag_sortation_out_detail
        self.error_table = CheckSqlStatement.check_t_bag_sortation_out_detail(self.oc_cursor,
                                                                              self.tracking_number_data,
                                                                              self.error_table)
        # aquarius.t_order_revenue_details
        self.error_table = CheckSqlStatement.check_t_order_revenue_details(self.oc_cursor,
                                                                           self.tracking_number_data,
                                                                           self.error_table)
        # aquarius.t_vendor_send_goods_prediction_detail
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction_detail(self.oc_cursor,
                                                                                         self.tracking_number_data,
                                                                                         self.error_table)
        # aquarius.t_vendor_send_goods_prediction
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction(self.oc_cursor,
                                                                                  self.tracking_number_data,
                                                                                  self.error_table)
        # aquarius.t_bag_first_leg_detail
        self.error_table = CheckSqlStatement.check_t_bag_first_leg_detail(self.oc_cursor,
                                                                          self.tracking_number_data,
                                                                          self.error_table)
        # aquarius.t_scan_package_abnormal
        self.error_table = CheckSqlStatement.check_t_scan_package_abnormal(self.oc_cursor,
                                                                           self.tracking_number_data,
                                                                           self.error_table)
        # aquarius.t_trace_eventcode_time
        self.error_table = CheckSqlStatement.check_t_trace_eventcode_time(self.oc_cursor,
                                                                          self.tracking_number_data,
                                                                          self.error_table)
        self.final_result["aquarius"] = self.error_table
        self.error_table = []
        self.oc_cursor.close_all()

    def check_rdc(self):
        dg_cursor = MysqlClient("pro_dg")  # dg数据库游标
        jx_cursor = MysqlClient("pro_jx")  # jx数据库游标
        hk_cursor = MysqlClient("pro_hk")  # hk数据库游标
        # t_waybill
        self.error_table = CheckSqlStatement.check_t_waybill(dg_cursor, self.tracking_number_data,
                                                             self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill(jx_cursor, self.tracking_number_data,
                                                             self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill(hk_cursor, self.tracking_number_data,
                                                             self.error_table)
        # t_last_mile_bag
        self.error_table = CheckSqlStatement.check_t_last_mile_bag(dg_cursor, self.tracking_number_data,
                                                                   self.error_table)
        self.error_table = CheckSqlStatement.check_t_last_mile_bag(jx_cursor, self.tracking_number_data,
                                                                   self.error_table)
        self.error_table = CheckSqlStatement.check_t_last_mile_bag(hk_cursor, self.tracking_number_data,
                                                                   self.error_table)
        # t_acas_inspect_bag_detail
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag_detail(dg_cursor, self.tracking_number_data,
                                                                             self.mawb_data,
                                                                             self.error_table)
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag_detail(jx_cursor, self.tracking_number_data,
                                                                             self.mawb_data,
                                                                             self.error_table)
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag_detail(hk_cursor, self.tracking_number_data,
                                                                             self.mawb_data,
                                                                             self.error_table)
        # t_acas_inspect_bag
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag(dg_cursor, self.tracking_number_data,
                                                                      self.error_table)
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag(jx_cursor, self.tracking_number_data,
                                                                      self.error_table)
        self.error_table = CheckSqlStatement.check_t_acas_inspect_bag(hk_cursor, self.tracking_number_data,
                                                                      self.error_table)
        # t_vendor_send_goods_prediction
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction(dg_cursor,
                                                                                  self.tracking_number_data,
                                                                                  self.error_table)
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction(jx_cursor,
                                                                                  self.tracking_number_data,
                                                                                  self.error_table)
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction(hk_cursor,
                                                                                  self.tracking_number_data,
                                                                                  self.error_table)
        # t_vendor_send_goods_prediction_detail
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction_detail(dg_cursor,
                                                                                         self.tracking_number_data,
                                                                                         self.error_table)
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction_detail(jx_cursor,
                                                                                         self.tracking_number_data,
                                                                                         self.error_table)
        self.error_table = CheckSqlStatement.check_t_vendor_send_goods_prediction_detail(hk_cursor,
                                                                                         self.tracking_number_data,
                                                                                         self.error_table)
        # t_out_bound_batch_package
        self.error_table = CheckSqlStatement.check_t_out_bound_batch_package(dg_cursor,
                                                                             self.tracking_number_data,
                                                                             self.error_table)
        self.error_table = CheckSqlStatement.check_t_out_bound_batch_package(jx_cursor,
                                                                             self.tracking_number_data,
                                                                             self.error_table)
        self.error_table = CheckSqlStatement.check_t_out_bound_batch_package(hk_cursor,
                                                                             self.tracking_number_data,
                                                                             self.error_table)
        # t_out_bound_batch
        self.error_table = CheckSqlStatement.check_t_out_bound_batch(dg_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        self.error_table = CheckSqlStatement.check_t_out_bound_batch(jx_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        self.error_table = CheckSqlStatement.check_t_out_bound_batch(hk_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        # t_scan_package_abnormal
        self.error_table = CheckSqlStatement.check_t_scan_package_abnormal(dg_cursor,
                                                                           self.tracking_number_data,
                                                                           self.error_table)
        self.error_table = CheckSqlStatement.check_t_scan_package_abnormal(jx_cursor,
                                                                           self.tracking_number_data,
                                                                           self.error_table)
        self.error_table = CheckSqlStatement.check_t_scan_package_abnormal(hk_cursor,
                                                                           self.tracking_number_data,
                                                                           self.error_table)
        # t_waybill_product
        self.error_table = CheckSqlStatement.check_t_waybill_product(dg_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_product(jx_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_product(hk_cursor,
                                                                     self.tracking_number_data,
                                                                     self.error_table)
        # t_waybill_process_expected
        self.error_table = CheckSqlStatement.check_t_waybill_process_expected(dg_cursor,
                                                                              self.tracking_number_data,
                                                                              self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_process_expected(jx_cursor,
                                                                              self.tracking_number_data,
                                                                              self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_process_expected(hk_cursor,
                                                                              self.tracking_number_data,
                                                                              self.error_table)
        # t_waybill_pickup
        self.error_table = CheckSqlStatement.check_t_waybill_pickup(dg_cursor,
                                                                    self.tracking_number_data,
                                                                    self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_pickup(jx_cursor,
                                                                    self.tracking_number_data,
                                                                    self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_pickup(hk_cursor,
                                                                    self.tracking_number_data,
                                                                    self.error_table)
        # t_waybill_consignee
        self.error_table = CheckSqlStatement.check_t_waybill_consignee(dg_cursor,
                                                                       self.tracking_number_data,
                                                                       self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_consignee(jx_cursor,
                                                                       self.tracking_number_data,
                                                                       self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_consignee(hk_cursor,
                                                                       self.tracking_number_data,
                                                                       self.error_table)
        # t_scan_package
        self.error_table = CheckSqlStatement.check_t_scan_package(dg_cursor,
                                                                  self.tracking_number_data,
                                                                  self.error_table)
        self.error_table = CheckSqlStatement.check_t_scan_package(jx_cursor,
                                                                  self.tracking_number_data,
                                                                  self.error_table)
        self.error_table = CheckSqlStatement.check_t_scan_package(hk_cursor,
                                                                  self.tracking_number_data,
                                                                  self.error_table)
        # t_scan_package_combine
        self.error_table = CheckSqlStatement.check_t_scan_package_combine(dg_cursor,
                                                                          self.tracking_number_data,
                                                                          self.error_table)
        self.error_table = CheckSqlStatement.check_t_scan_package_combine(jx_cursor,
                                                                          self.tracking_number_data,
                                                                          self.error_table)
        self.error_table = CheckSqlStatement.check_t_scan_package_combine(hk_cursor,
                                                                          self.tracking_number_data,
                                                                          self.error_table)
        # t_waybill_feedback_error
        self.error_table = CheckSqlStatement.check_t_waybill_feedback_error(dg_cursor,
                                                                            self.tracking_number_data,
                                                                            self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_feedback_error(jx_cursor,
                                                                            self.tracking_number_data,
                                                                            self.error_table)
        self.error_table = CheckSqlStatement.check_t_waybill_feedback_error(hk_cursor,
                                                                            self.tracking_number_data,
                                                                            self.error_table)
        # t_dhl_bag_outbound
        self.error_table = CheckSqlStatement.check_t_dhl_bag_outbound(dg_cursor,
                                                                      self.tracking_number_data,
                                                                      self.error_table)
        self.error_table = CheckSqlStatement.check_t_dhl_bag_outbound(jx_cursor,
                                                                      self.tracking_number_data,
                                                                      self.error_table)
        self.error_table = CheckSqlStatement.check_t_dhl_bag_outbound(hk_cursor,
                                                                      self.tracking_number_data,
                                                                      self.error_table)
        dg_cursor.close_all()
        jx_cursor.close_all()
        hk_cursor.close_all()
        self.final_result["rdc"] = self.error_table  # 暂时不区分rdc
        self.error_table = []

    def check_fin_gemini(self):
        ge_cursor = MysqlClient("pro_gemini")  # gemini数据库游标
        # gemini.t_fin_trade_detail
        self.error_table = CheckSqlStatement.check_t_fin_trade_detail(ge_cursor, self.tracking_number_data,
                                                                      self.error_table)
        # gemini.t_fin_out_business
        self.error_table = CheckSqlStatement.check_t_fin_out_business(ge_cursor, self.tracking_number_data,
                                                                      self.error_table)
        self.final_result["gemini"] = self.error_table
        self.error_table = []
        ge_cursor.close_all()

    def check_fin_taurus(self):
        ta_cursor = MysqlClient("pro_taurus")  # taurus数据库游标
        # taurus.t_fin_trade_detail
        self.error_table = CheckSqlStatement.check_t_fin_trade_detail(ta_cursor, self.tracking_number_data,
                                                                      self.error_table)
        # taurus.t_fin_out_business
        self.error_table = CheckSqlStatement.check_t_fin_out_business(ta_cursor, self.tracking_number_data,
                                                                      self.error_table)
        self.final_result["taurus"] = self.error_table
        self.error_table = []
        ta_cursor.close_all()

    def check_all(self):
        self.check_aq()
        self.check_rdc()
        self.check_fin_gemini()
        self.check_fin_taurus()
        return self.final_result, self.data_len, self.tracking_number_data_list, self.mawb_list


if __name__ == '__main__':
    check = CheckSql("../data/sql_data/2021-12-21sql_sata.xlsx")
    print(check.check_all())
