import enum

from rest_framework.response import Response
from rest_framework import status

# https://juejin.cn/post/7307502467826008091
from abc import ABC
from collections.abc import MutableMapping


# class BaseResult(object):
#
#     def __init__(self, code=0, message="操作成功", data=None, *args, **kwargs):
#         self.__success = True
#         self.code = code
#         self.message = message
#         self.data = data
#
#     def success(self, code=0, message="操作成功", data=None, result_enum=ResultEnum.SUCCESS, *args, **kwargs):
#         self.data = data
#         if isinstance(result_enum, ResultEnum):
#             code, message = result_enum.value
#         self.code = code
#         self.message = message
#         print(self.__dict__)
#         return Response(data=self.serializer, status=status.HTTP_200_OK)
#
#     def failure(self, code=9999, message="操作失败", data=None, result_enum=ResultEnum.FAILURE, *args, **kwargs):
#         self.__success = False
#         self.data = data
#         if isinstance(result_enum, ResultEnum):
#             code, message = result_enum.value
#         self.code = code
#         self.message = message
#         self.data = data
#         return Response(data=self.serializer, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     @property
#     def serializer(self):
#         return dict(code=self.code, success=self.__success, message=self.message, data=self.data)


class ResultEnum(enum.Enum):
    success = ("0000", '操作成功')
    exception = ('5000', '业务逻辑异常')
    validate = ('4000', '参数异常')
    failure = ("9999", '操作失败')

    @property
    def code(self):
        code, _ = self.value
        return code

    @property
    def message(self):
        _, message = self.value
        return message


class BaseResult(dict):

    def __init__(self, message='成功', data=None, *args, **kwargs):
        super(BaseResult, self).__init__()
        if kwargs:
            data = self.get('data') or dict()
            data.update(kwargs)
        self.update(success=True, message=message, data=data)

    def success(self, message='操作成功', data=None, **kwargs):
        self.update(success=True, message=message, data=data)
        return self

    def failure(self, message='操作失败', data=None, **kwargs):
        self.update(success=False, message=message, data=data)
        return self

    @property
    def message(self): return self.get('message')

    @property
    def ok(self): return self.get('success')

    @property
    def data(self): return self.get('data')


class _BizResult(BaseResult):

    def success(self, message='操作成功', data=None, result_enum=None, **kwargs):
        # data = data if data else dict()
        # data.update(**kwargs)
        if isinstance(result_enum, ResultEnum):
            self.update(success=True, code=result_enum.code, message=result_enum.message, data=data)
        else:
            self.update(success=True, message=message, data=data)

        return self

    def failure(self, message='操作失败', data=None, result_enum=None, **kwargs):
        if isinstance(result_enum, ResultEnum):
            self.update(success=False, code=result_enum.code, message=result_enum.message, data=data)
        else:
            self.update(success=False, message=message, data=data)
        return self


class BaseApiResult(BaseResult):

    def success(self, code=ResultEnum.success.code, message=ResultEnum.success.message, data=None, **kwargs):
        self.update(code=code, success=True, message=message, data=data)
        return Response(data=self, status=status.HTTP_200_OK)

    def failure(self, code=ResultEnum.failure.code, message=ResultEnum.failure.message, data=None, result_enum=None,
                **kwargs):
        if isinstance(result_enum, ResultEnum):
            self.update(success=False, code=result_enum.code, message=result_enum.message, data=data)
        else:
            self.update(code=code, success=False, message=message, data=data)
        return Response(data=self, status=status.HTTP_200_OK)


BizResult = _BizResult()
# BizResult.success()


ApiResult = BaseApiResult()
