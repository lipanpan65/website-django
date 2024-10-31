import enum

from rest_framework.response import Response
from rest_framework import status

# https://juejin.cn/post/7307502467826008091
from abc import ABC
from collections.abc import MutableMapping

# class BaseResult(dict):
#
#     def __init__(self, message='成功', data=None, *args, **kwargs):
#         super(BaseResult, self).__init__()
#         if kwargs:
#             data = self.get('data') or dict()
#             data.update(kwargs)
#         self.update(success=True, message=message, data=data)
#
#     def success(self, message='操作成功', data=None, **kwargs):
#         self.update(success=True, message=message, data=data)
#         return self
#
#     def failure(self, message='操作失败', data=None, **kwargs):
#         self.update(success=False, message=message, data=data)
#         return self
#
#     @property
#     def message(self): return self.get('message')
#
#     @property
#     def ok(self): return self.get('success')
#
#     @property
#     def data(self): return self.get('data')


# class _BizResult(BaseResult):
#
#     def success(self, message='操作成功', data=None, result_enum=None, **kwargs):
#         # data = data if data else dict()
#         # data.update(**kwargs)
#         if isinstance(result_enum, ResultEnum):
#             self.update(success=True, code=result_enum.code, message=result_enum.message, data=data)
#         else:
#             self.update(success=True, message=message, data=data)
#
#         return self
#
#     def failure(self, message='操作失败', data=None, result_enum=None, **kwargs):
#         if isinstance(result_enum, ResultEnum):
#             self.update(success=False, code=result_enum.code, message=result_enum.message, data=data)
#         else:
#             self.update(success=False, message=message, data=data)
#         return self


# class BaseApiResult(BaseResult):
#
#     def success(self, code=ResultEnum.success.code, message=ResultEnum.success.message, data=None, **kwargs):
#         self.update(code=code, success=True, message=message, data=data)
#         return Response(data=self, status=status.HTTP_200_OK)
#
#     def failure(self, code=ResultEnum.failure.code, message=ResultEnum.failure.message, data=None, result_enum=None,
#                 **kwargs):
#         if isinstance(result_enum, ResultEnum):
#             self.update(success=False, code=result_enum.code, message=result_enum.message, data=data)
#         else:
#             self.update(code=code, success=False, message=message, data=data)
#         return Response(data=self, status=status.HTTP_200_OK)


import enum
from rest_framework.response import Response
from rest_framework import status


class ResultEnum(enum.Enum):
    SUCCESS = ("0000", '操作成功')
    EXCEPTION = ('5000', '业务逻辑异常')
    VALIDATE = ('4000', '参数异常')
    FAILURE = ("9999", '操作失败')

    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[1]


class BaseResult(dict):
    def __init__(self, success=True, message='成功', data=None, code=None, **kwargs):
        super(BaseResult, self).__init__()
        # 初始化时，允许附加额外的数据
        data = data or {}
        data.update(kwargs)
        self.update(success=success, message=message, data=data)
        if code:
            self.update(code=code)

    def success(self, message='操作成功', data=None, code=ResultEnum.SUCCESS.code, **kwargs):
        """成功响应"""
        data = data or {}
        self.update(success=True, message=message, data=data, code=code)
        return self

    def failure(self, message='操作失败', data=None, code=ResultEnum.FAILURE.code, **kwargs):
        """失败响应"""
        data = data or {}
        self.update(success=False, message=message, data=data, code=code)
        return self


class BaseBizResult(BaseResult):
    def success(self, message='操作成功', data=None, result_enum=None, **kwargs):
        """处理业务逻辑成功的返回"""
        if isinstance(result_enum, ResultEnum):
            return super().success(message=result_enum.message, data=data, code=result_enum.code, **kwargs)
        return super().success(message=message, data=data, **kwargs)

    def failure(self, message='操作失败', data=None, result_enum=None, **kwargs):
        """处理业务逻辑失败的返回"""
        if isinstance(result_enum, ResultEnum):
            return super().failure(message=result_enum.message, data=data, code=result_enum.code, **kwargs)
        return super().failure(message=message, data=data, **kwargs)


class BaseApiResult(BaseResult):
    def success(self, message=ResultEnum.SUCCESS.message, data=None, code=ResultEnum.SUCCESS.code, **kwargs):
        """API 成功响应"""
        response_data = super().success(message=message, data=data, code=code, **kwargs)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def failure(self, message=ResultEnum.FAILURE.message, data=None, code=ResultEnum.FAILURE.code, result_enum=None,
                **kwargs):
        """API 失败响应"""
        if result_enum and isinstance(result_enum, ResultEnum):
            response_data = super().failure(message=result_enum.message, data=data, code=result_enum.code, **kwargs)
        else:
            response_data = super().failure(message=message, data=data, code=code, **kwargs)
        return Response(data=response_data, status=status.HTTP_200_OK)


# # 使用示例
BizResult = BaseBizResult()
ApiResult = BaseApiResult()
