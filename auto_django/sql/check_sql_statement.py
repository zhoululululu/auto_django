# -*- coding: utf-8 -*- 
"""
Created on 2021/12/1 11:32 
@File  : check_sql_statement.py
@author: zhoulu
@Desc  :
"""


class CheckSqlStatement(object):
    @classmethod
    def add_error(cls, result, table, result_list):
        if result != 0:
            result_list.append(table)

    @classmethod
    def check_t_waybill(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill", result_list)
        return result_list

    @classmethod
    def check_t_waybill_product(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_product "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_product", result_list)
        return result_list

    @classmethod
    def check_t_waybill_process_expected(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_process_expected "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_process_expected", result_list)
        return result_list

    @classmethod
    def check_t_waybill_pickup(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_pickup "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_pickup", result_list)
        return result_list

    @classmethod
    def check_t_waybill_consignee(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_consignee "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_consignee", result_list)
        return result_list

    @classmethod
    def check_t_waybill_sorting(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_sorting "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_sorting", result_list)
        return result_list

    @classmethod
    def check_t_waybill_combine(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_combine "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_combine", result_list)
        return result_list

    @classmethod
    def check_t_acas_inspect_bag_detail(cls, cursor, tracking_number_list, mawb_list, result_list):
        sentence_2 = "" if len(mawb_list) == 0 else " or mawb in %s " % str(mawb_list)
        result = cursor.execute_sql("select count(*) from t_acas_inspect_bag_detail "
                                    "where tracking_number in %s " %
                                    str(tracking_number_list)
                                    + sentence_2 + "and  is_active=1; ")[0][0]
        cls.add_error(result, "t_acas_inspect_bag_detail", result_list)
        return result_list

    @classmethod
    def check_t_acas_inspect_bag(cls, cursor, mawb_list, result_list):
        if len(mawb_list) != 0:
            result = cursor.execute_sql("select count(*) from t_acas_inspect_bag "
                                        "where mawb in %s and  is_active=1;" % str(mawb_list))[0][0]
            cls.add_error(result, "t_acas_inspect_bag", result_list)
        return result_list

    @classmethod
    def check_t_bag_sortation_out_combine_detail(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_sortation_out_combine_detail as a "
                                    "join t_waybill_sorting as b "
                                    "on a.parcel_tracking_number = b.last_mile_tracking_number "
                                    "where b.tracking_number in %s "
                                    "and a.is_active = 1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_sortation_out_combine_detail", result_list)
        return result_list

    @classmethod
    def check_t_bag_sortation_out_combine(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_sortation_out_combine as a "
                                    "join t_bag_sortation_out_combine_detail as b "
                                    "join t_waybill_sorting as c "
                                    "on b.parcel_tracking_number = c.last_mile_tracking_number "
                                    "and  a.medium_package_id = b.medium_package_id "
                                    "where c.tracking_number in %s "
                                    "and a.is_active = 1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_sortation_out_combine", result_list)
        return result_list

    @classmethod
    def check_t_waybill_sorting_combine(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_sorting_combine "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_sorting_combine", result_list)
        return result_list

    @classmethod
    def check_t_bag_vendor_dhl(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_vendor_dhl as a "
                                    "join t_bag_vendor_detail_dhl as b "
                                    "on a.bag_no = b.bag_no "
                                    "where b.tracking_number in %s "
                                    "and a.is_active = 1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_vendor_dhl", result_list)
        return result_list

    @classmethod
    def check_t_bag_vendor_detail_dhl(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_vendor_detail_dhl "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_vendor_detail_dhl", result_list)
        return result_list

    @classmethod
    def check_t_bag_sortation_out(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_sortation_out as a "
                                    "join t_bag_sortation_out_detail as b "
                                    "on a.bag_id = b.bag_id "
                                    "where b.tracking_number in %s "
                                    "and a.is_active = 1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_sortation_out", result_list)
        return result_list

    @classmethod
    def check_t_bag_sortation_out_detail(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_sortation_out_detail "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_sortation_out_detail", result_list)
        return result_list

    @classmethod
    def check_t_order_revenue_details(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_order_revenue_details "
                                    "where order_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_order_revenue_details", result_list)
        return result_list

    @classmethod
    def check_t_vendor_send_goods_prediction_detail(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_vendor_send_goods_prediction_detail "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_vendor_send_goods_prediction_detail", result_list)
        return result_list

    @classmethod
    def check_t_vendor_send_goods_prediction(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_vendor_send_goods_prediction as a "
                                    "join t_vendor_send_goods_prediction_detail as b "
                                    "on a.bag_id = b.bag_id "
                                    "where b.tracking_number in %s "
                                    "and a.is_active = 1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_vendor_send_goods_prediction", result_list)
        return result_list

    @classmethod
    def check_t_bag_first_leg_detail(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_bag_first_leg_detail "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_bag_first_leg_detail", result_list)
        return result_list

    @classmethod
    def check_t_scan_package_abnormal(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_scan_package_abnormal "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_scan_package_abnormal", result_list)
        return result_list

    @classmethod
    def check_t_trace_eventcode_time(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_trace_eventcode_time "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_trace_eventcode_time", result_list)
        return result_list

    @classmethod
    def check_t_last_mile_bag(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_last_mile_bag as a "
                                    "join t_scan_package as b "
                                    "on a.bag_no = b.lastmile_bag_no "
                                    "where b.tracking_number in %s "
                                    "and a.is_active=1" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_last_mile_bag", result_list)
        return result_list

    @classmethod
    def check_t_out_bound_batch_package(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_out_bound_batch_package as a "
                                    "join t_scan_package as b "
                                    "on a.package_no = b.lastmile_bag_no "
                                    "where b.tracking_number in %s "
                                    "and a.is_active=1" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_out_bound_batch_package", result_list)
        return result_list

    @classmethod
    def check_t_out_bound_batch(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_out_bound_batch as a "
                                    "join t_out_bound_batch_package as b "
                                    "join t_scan_package as c "
                                    "on b.package_no = c.lastmile_bag_no "
                                    "and a.batch_id = b.batch_id "
                                    "where c.tracking_number in %s "
                                    "and a.is_active=1" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_out_bound_batch", result_list)
        return result_list

    @classmethod
    def check_t_scan_package(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_scan_package "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_scan_package", result_list)
        return result_list

    @classmethod
    def check_t_scan_package_combine(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_scan_package_combine "
                                    "where tracking_number in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_scan_package_combine", result_list)
        return result_list

    @classmethod
    def check_t_waybill_feedback_error(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_waybill_feedback_error as a "
                                    "join t_scan_package as b "
                                    "on a.business_id = b.lastmile_bag_no "
                                    "or a.business_id = b.tracking_number "
                                    "where b.tracking_number in %s "
                                    "and a.is_active=1" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_waybill_feedback_error", result_list)
        return result_list

    @classmethod
    def check_t_dhl_bag_outbound(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_dhl_bag_outbound as a "
                                    "join t_dhl_bag_outbound_detail as b "
                                    "on a.dhl_bag_no = b.bag_no "
                                    "where b.tracking_number in %s "
                                    "and a.is_active=1" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_dhl_bag_outbound", result_list)
        return result_list

    @classmethod
    def check_t_fin_trade_detail(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_fin_trade_detail "
                                    "where trade_id in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_fin_trade_detail", result_list)
        return result_list

    @classmethod
    def check_t_fin_out_business(cls, cursor, tracking_number_list, result_list):
        result = cursor.execute_sql("select count(*) from t_fin_out_business "
                                    "where trade_id in %s and is_active=1;" % str(tracking_number_list))[0][0]
        cls.add_error(result, "t_fin_out_business", result_list)
        return result_list
