from __future__ import annotations
from typing import Any, Optional, TypedDict, Union
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList

import enum


# 定义响应类型
class ResultDict(TypedDict):
    code: str
    success: bool
    message: str
    data: dict[str, Any]

# 错误码枚举
class ResultEnum(enum.Enum):
    SUCCESS = ("0000", '操作成功')
    EXCEPTION = ('5000', '业务逻辑异常')
    VALIDATE = ('4000', '参数异常')
    FAILURE = ("9999", '操作失败')

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]


# 基础响应构建器
class BaseResultBuilder:
    def __init__(self, success: bool, code: str, message: str, data: Optional[dict] = None):
        self._data: ResultDict = {
            "code": code,
            "success": success,
            "message": message,
            "data": data if data is not None else {}
        }

    def with_data(self, **kwargs) -> 'BaseResultBuilder':
        """添加额外数据字段"""
        if 'data' in kwargs:
            data_value = kwargs.pop('data')
            # 处理字典类型
            if isinstance(data_value, dict):
                self._data["data"].update(data_value)
            # 处理 ReturnList 类型
            elif isinstance(data_value, ReturnList):
                # 将 ReturnList 中的元素逐个合并到 data 字典
                if 'page' in kwargs:
                    self._data["data"] = dict(page=kwargs.pop('page'),data=data_value)
            # 处理其他可迭代类型
            elif hasattr(data_value, '__iter__'):
                for item in data_value:
                    if isinstance(item, dict):
                        self._data["data"].update(item)
            # 其他类型处理
            else:
                # 这里可以根据需要处理其他类型，例如将单个值存入指定键
                self._data["data"]["raw_data"] = data_value
        # 处理剩余的键值对
        self._data["data"].update(kwargs)
        return self

    def build(self) -> ResultDict:
        """构建最终响应字典"""
        return self._data


# 业务逻辑响应
class BizResult:
    @staticmethod
    def success(result_enum: ResultEnum = ResultEnum.SUCCESS, **kwargs) -> ResultDict:
        """成功响应构建器"""
        data = kwargs.pop('data', {})
        return BaseResultBuilder(
            success=True,
            code=result_enum.code,
            message=result_enum.message
        ).with_data(**data, **kwargs).build()

    @staticmethod
    def failure(result_enum: ResultEnum = ResultEnum.FAILURE, **kwargs) -> ResultDict:
        """失败响应构建器"""
        return BaseResultBuilder(
            success=False,
            code=result_enum.code,
            message=result_enum.message
        ).with_data(**kwargs).build()


# API响应包装
class ApiResult:
    @staticmethod
    def success(result_enum: ResultEnum = ResultEnum.SUCCESS, **kwargs) -> Response:
        """成功API响应"""
        return Response(
            data=BizResult.success(result_enum, **kwargs),
            status=status.HTTP_200_OK
        )

    @staticmethod
    def failure(result_enum: ResultEnum = ResultEnum.FAILURE, **kwargs) -> Response:
        """失败API响应"""
        return Response(
            data=BizResult.failure(result_enum, **kwargs),
            status=status.HTTP_200_OK
        )


# 使用示例
if __name__ == "__main__":
    # 业务逻辑使用
    biz_success = BizResult.success(ResultEnum.SUCCESS, user="admin")
    print(biz_success)

    biz_failure = BizResult.failure(ResultEnum.VALIDATE, error="invalid email")
    print(biz_failure)

    # API接口使用
    api_success = ApiResult.success(ResultEnum.SUCCESS, count=100)
    print(api_success.data)

    api_failure = ApiResult.failure(ResultEnum.EXCEPTION, details="database error")
    print(api_failure.data)
