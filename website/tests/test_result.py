# -*- coding: utf-8 -*-
# @Time        : 2024/3/19
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : test_result.py

from collections import UserDict


class BaseResult(object):

    def __init__(self, code=0, success=True, message='操作成功', data=None, /, **kwargs):
        self.code = code
        self.data = data
        self.message = message
        self.__data = dict(code=code, message=message, data=data)
        if kwargs:
            self.__data.update(kwargs)

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        return repr(self.__data)

    def __iter__(self):
        return iter(self.__data)

    @classmethod
    def success(cls):
        print(cls)
        pass


print(BaseResult.success())

r = BaseResult()

for i in r:
    print(i)
