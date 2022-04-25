# -*- coding: utf-8 -*- 
"""
Created on 2021/10/18 10:43 
@File  : get_regular.py
@author: zhoul
@Desc  :
"""

import re

from commonfunc.get_logging import Logging

logger = Logging()


class GetRegular(object):

    @classmethod
    def get_regular_result(cls, regx, data):
        result_count, data_length, error_data = 0, len(data), []
        for i in data:
            try:
                pattern = re.compile(regx)  # re.I 表示忽略大小写
                if pattern.match(i) is not None:
                    m = pattern.match(i).group()
                    result_count += 1 if m != 0 else 0
                else:
                    result_count += 0
                    error_data.append(i)
                    logger.error("未匹配到正则：%s" % i)
            except Exception as e:
                logger.error("报错：%s" % e)
        return data_length, result_count, error_data

# if __name__ == '__main__':
#     GetRegular.get_regular_result(
#         "^63086$|^630[\s|\r\n]*86$|^[G|g][R|r]-63086$|^[G|g][R|r]-630[\s|\r\n]*86$|^[G|g][R|r]63086$|^[G|g][R|r]630[\s|\r\n]*86$",
#         ["630 86", "63086", "gr63086", "11"])
