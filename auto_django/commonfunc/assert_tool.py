# -*- coding: utf-8 -*- 
"""
Created on 2021/7/2 13:57 
@File  : assert_tool.py
@author: zhoul
@Desc  :
"""
import re
import filecmp
import os
import jsonpath
import json


class AssertTool(object):
    @classmethod
    def is_regular_match(cls, source_str, regular_str):
        """
        判断字符串是否符合正则表达式，正则表达式的内容包含正则关键字需用\进行转移
        :param source_str:
        :param regular_str:
        :return:
        """
        if re.match(regular_str, source_str):
            return True
        else:
            return False

    @classmethod
    def is_files_equal(cls, file_path1, file_path2):
        """
        比较两个文件内容是否一样
        :param file_path1:
        :param file_path2:
        :return:
        """
        if filecmp.cmp(file_path1, file_path2):
            return True
        else:
            return False

    @classmethod
    def is_files_size_equal(cls, file_path1, file_path2):
        """
        比较两个文件大小是否一致
        :param file_path2:
        :param file_path1:
        :return:
        """
        size1 = os.path.getsize(file_path1)
        size2 = os.path.getsize(file_path2)
        if size1 == size2:
            return True
        else:
            return False

    @classmethod
    def compare_dict(cls, act_value, exp_value, ignore=None, retain=None):
        """
        校验结果
        :param act_value: 实际的接口返回结果
        :param exp_value: 预期的接口返回结果
        :param ignore: 需要忽略的json key值（注意哦，这一单忽略，就遍历只要碰见这个key值就忽略）
        :param retain: 需要校验的值
        :return:
        """
        try:
            if retain != "":
                value = []
                if retain == ".":
                    pass
                else:
                    for i in (eval(retain)):
                        value.append(jsonpath.jsonpath(act_value, i))
                    act_value = value
                    exp_value = eval(exp_value)
            else:
                exp_value = json.loads(exp_value)
                for key in eval(ignore):
                    if act_value.__contains__(key):
                        act_value.__delitem__(key)
                        exp_value.__delitem__(key)
            if act_value == exp_value:
                return True, exp_value, act_value
            else:
                return False, exp_value, act_value
        except Exception as e:
            assert False, "校验出错"