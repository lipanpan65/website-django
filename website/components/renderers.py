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
        if renderer_context and renderer_context.get('response'):
            response = renderer_context.get('response')
            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                if isinstance(data, dict):
                    if 'success' in data.keys() or 'code' in data.keys():
                        return super().render(data, accepted_media_type, renderer_context)
                data = BizResult.success(data=data)
                data.update(code=ResultEnum.success.code)
                return super().render(data, accepted_media_type, renderer_context)
            else:
                pass
        return super().render(data, accepted_media_type, renderer_context)
