# -*- coding: utf-8 -*-
# @Time        : 2024/3/16
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : test_string_utils.py
import unittest


class StringUtils(object):

    @staticmethod
    def is_empty(s: str) -> bool:
        """
        校验字符串是否为有效的字符串
        """
        if s is not None and bool(s.strip()) and s.strip() not in ['null']:
            return True
        return False


# class StringUtilsUnitTest(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_is_empty(self):
#         pass

r = StringUtils.is_empty('null')
r = StringUtils.is_empty(None)
r = StringUtils.is_empty('')
r = StringUtils.is_empty("not empty")
print(r)
