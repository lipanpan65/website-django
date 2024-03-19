import enum

from rest_framework.response import Response
from rest_framework import status


class ResultEnum(enum.Enum):
    SUCCESS = (0, '操作成功')

    FAILURE = (9999, '操作失败')


class BaseResult(object):

    def __init__(self, code=0, message="操作成功", data=None, *args, **kwargs):
        self.__success = True
        self.code = code
        self.message = message
        self.data = data

    def success(self, code=0, message="操作成功", data=None, result_enum=ResultEnum.SUCCESS, *args, **kwargs):
        self.data = data
        if isinstance(result_enum, ResultEnum):
            code, message = result_enum.value
        self.code = code
        self.message = message
        print(self.__dict__)
        return Response(data=self.serializer, status=status.HTTP_200_OK)

    def failure(self, code=9999, message="操作失败", data=None, result_enum=ResultEnum.FAILURE, *args, **kwargs):
        self.__success = False
        self.data = data
        if isinstance(result_enum, ResultEnum):
            code, message = result_enum.value
        self.code = code
        self.message = message
        self.data = data
        return Response(data=self.serializer, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @property
    def serializer(self):
        return dict(code=self.code, success=self.__success, message=self.message, data=self.data)


Result = BaseResult()
