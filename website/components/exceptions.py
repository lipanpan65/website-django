import logging

import rest_framework.exceptions

from components.response import BizResult, ResultEnum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as origin_exception_handler

logger = logging.getLogger()


# https://juejin.cn/post/6976496971368366116
# https://q1mi.github.io/Django-REST-framework-documentation/api-guide/exceptions_zh/

class BizException(RuntimeError):
    """
    自定义业务逻辑异常
    """

    status_code = status.HTTP_200_OK

    def __init__(self,
                 code=ResultEnum.exception.code,
                 message=ResultEnum.exception.message, result_enum=None):
        self.message = message
        self.code = code
        if isinstance(result_enum, ResultEnum):
            self.code = result_enum.code
            self.message = result_enum.message
        super().__init__(message)

        logger.error("[BizException] %s %s" % (self.code, self.message))


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    # 这里对自定义的 CustomException 直接返回，保证系统其他异常不受影响
    if isinstance(exc, rest_framework.exceptions.ValidationError):
        print('----------')
        print(exc)  # TODO 打印校验的异常信息，重复更新了，如果被拦截了还会走 全局定义的 response
        print('----------')
        data = BizResult.failure(result_enum=ResultEnum.validate)
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        response = origin_exception_handler(exc, context)
        return response
    # if isinstance(exc, BizException):
    #     print(exc)
    #     return Response(data=exc.data, status=exc.status_code)
