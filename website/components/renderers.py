# -*- coding: utf-8 -*-
# @Time        : 2024/3/29
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : renders.py

from rest_framework import status
from rest_framework.renderers import JSONRenderer as OriginJSONRenderer
from components.response import ApiResult, BizResult, ResultEnum
from typing import Dict, Any, Optional

class JSONRenderer(OriginJSONRenderer):
    def render(self, data: Any, accepted_media_type: Optional[str] = None, renderer_context: Optional[Dict[str, Any]] = None) -> bytes:
        """
        重写 render 方法，对响应数据进行包装处理。

        :param data: 要渲染的数据
        :param accepted_media_type: 客户端接受的媒体类型
        :param renderer_context: 渲染上下文，包含视图、请求、响应等信息
        :return: 渲染后的字节数据
        """
        # 获取响应对象
        response = self.get_response(renderer_context)
        if not response:
            return super().render(data, accepted_media_type, renderer_context)

        # 处理成功响应
        if self.is_success_response(response):
            response.status_code = status.HTTP_200_OK
            if self.is_custom_response(data):
                return super().render(data, accepted_media_type, renderer_context)
            # 包装成功的响应数据
            data = self.wrap_success_data(data)
        return super().render(data, accepted_media_type, renderer_context)

    def get_response(self, renderer_context: Optional[Dict[str, Any]]) -> Optional[Any]:
        """
        从渲染上下文中获取响应对象。

        :param renderer_context: 渲染上下文
        :return: 响应对象，如果不存在则返回 None
        """
        return renderer_context.get('response') if renderer_context else None

    def is_success_response(self, response: Any) -> bool:
        """
        判断响应是否为成功响应。

        :param response: 响应对象
        :return: 如果是成功响应返回 True，否则返回 False
        """
        return response.status_code in {status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT}

    def is_custom_response(self, data: Any) -> bool:
        """
        判断数据是否为自定义响应（包含 'success' 和 'code' 字段）。

        :param data: 要判断的数据
        :return: 如果是自定义响应返回 True，否则返回 False
        """
        return isinstance(data, dict) and {'success', 'code'}.intersection(data)

    def wrap_success_data(self, data: Any) -> Dict[str, Any]:
        """
        包装成功的响应数据。

        :param data: 要包装的数据
        :return: 包装后的字典数据
        """
        result = BizResult.success(data=data)
        result['code'] = ResultEnum.SUCCESS.code
        return result