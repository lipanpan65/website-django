import logging
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as origin_exception_handler

from components.response import BizResult, ResultEnum

logger = logging.getLogger(__name__)


class BizException(RuntimeError):
    """
    自定义业务逻辑异常
    """
    status_code = status.HTTP_200_OK

    def __init__(self, code=ResultEnum.EXCEPTION.code, message=ResultEnum.EXCEPTION.message, result_enum=None):
        if isinstance(result_enum, ResultEnum):
            code, message = result_enum.code, result_enum.message

        self.code = code
        self.message = message
        super().__init__(self.message)

        logger.error(f"[BizException] Code: {self.code}, Message: {self.message}")


def exception_handler(exc, context):
    """
    全局异常处理函数，捕获并处理自定义和框架异常。
    """
    # 处理 ValidationError
    # 处理 ValidationError
    if isinstance(exc, exceptions.ValidationError):
        logger.warning(f"Validation Error: {exc}")

        # 提取详细的错误信息
        error_details = exc.detail if hasattr(exc, 'detail') else str(exc)

        # 将错误信息包含在响应数据中
        data = BizResult.failure(
            # message=ResultEnum.VALIDATE.message,
            data=error_details,
            result_enum=ResultEnum.VALIDATE
        )
        return Response(data=data, status=status.HTTP_200_OK)

    # 处理 BizException
    if isinstance(exc, BizException):
        logger.error(f"Business Exception: {exc}")
        data = BizResult.failure(code=exc.code, message=exc.message)
        return Response(data=data, status=exc.status_code)

    # 处理其他异常
    response = origin_exception_handler(exc, context)
    if response is None:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        data = BizResult.failure(message="服务器内部错误", result_enum=ResultEnum.FAILURE)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
