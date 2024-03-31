# -*- coding: utf-8 -*-
# @Time        : 2024/3/30
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : test_result_enum.py

import enum


class ResultEnum(enum.Enum):
    success = ("0000", '操作成功')
    exception = ('5000', '业务逻辑异常')
    failure = ("9999", '操作失败')

    @property
    def code(self):
        code, _ = self.value
        return code

    @property
    def message(self):
        _, message = self.value
        return message


# code = ResultEnum.success.code
# message = ResultEnum.success.message
# result_enum = ResultEnum.failure
# print('-----------')
# print(result_enum.code)
# print(result_enum.message)
# print('-----------')
# print(isinstance(result_enum, ResultEnum))
#
# print(code, message)
