# -*- coding: utf-8 -*-
# @Time        : 2024/3/29
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : renders.py

from rest_framework import status
from rest_framework.renderers import JSONRenderer as OriginJSONRenderer
from components.response import ApiResult, BizResult, ResultEnum

"""
renderer_context {
    'view': <blog.views.ArticleViewSet object at 0x106f0ad90>, 
    'args': (), 
    'kwargs': {}, 
    'request': <rest_framework.request.Request: GET '/api/user/v1/article/'>, 
    'response': <Response status_code=200, "application/json">
}

"""


class JSONRenderer(OriginJSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None

        # 确保 response 存在
        if not response:
            return super().render(data, accepted_media_type, renderer_context)

        # 处理成功响应的情况
        if response.status_code in {status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT}:
            response.status_code = status.HTTP_200_OK
            if isinstance(data, dict) and {'success', 'code'}.intersection(data):
                return super().render(data, accepted_media_type, renderer_context)

            # 包装成功的响应数据
            data = BizResult.success(data=data)
            data['code'] = ResultEnum.SUCCESS.code
            return super().render(data, accepted_media_type, renderer_context)

        # 其他情况
        return super().render(data, accepted_media_type, renderer_context)
