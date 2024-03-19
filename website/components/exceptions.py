from components.response import Result, ResultEnum
from rest_framework import status
from rest_framework.views import exception_handler


# class BizException(RuntimeError):
#     """
#     自定义业务逻辑异常
#     """
#
#     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#
#     def __init__(self, biz_enum):
#         code, message = biz_enum.value
#         super(BizException, self).__init__(message)
#         self.message = message
#         self.code = code
