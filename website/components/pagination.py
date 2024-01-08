# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 5:30 下午
# @Author  : lipanpan65
# @Email  : 1299793997@qq.com
# @File  : pagination.py
# @Desc :
# {
#     page: {
#         current: 1,
#         total: 20,
#         page_size: 10
#     },
#     data: []
# }


from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class TablePageNumberPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', {
                'total': self.page.paginator.count,
                'current': self.page.number,
                'pageSize': self.page.paginator.per_page,
            }),
            ('data', data)
        ]))


class SizeTablePageNumberPagination(TablePageNumberPagination):
    page_size_query_param = 'page_size'
