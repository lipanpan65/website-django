# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 5:30 下午
# @Author  : lipanpan
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
from components.response import BizResult, ResultEnum


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

    # def get_paginated_response(self, data):
    #     return Response(
    #         BizResult.success(result_enum=ResultEnum.success, data=OrderedDict([
    #             ('page', {
    #                 'total': self.page.paginator.count,
    #                 'current': self.page.number,
    #                 'pageSize': self.page.paginator.per_page,
    #             }),
    #             ('data', data)
    #         ]))
    #     )


class SizeTablePageNumberPagination(TablePageNumberPagination):
    page_size_query_param = 'page_size'

    # def get_paginated_response(self, data):
    #     data = BizResult.success(result_enum=ResultEnum.success, data=OrderedDict([
    #         ('page', {
    #             'total': self.page.paginator.count,
    #             'current': self.page.number,
    #             'pageSize': self.page.paginator.per_page,
    #         }),
    #         ('data', data)
    #     ]))
    #     print('data', data)
    #     return Response(data=data)

        # page_data = OrderedDict([
        #     ('page', {
        #         'total': self.page.paginator.count,
        #         'current': self.page.number,
        #         'pageSize': self.page.paginator.per_page,
        #     }),
        #     ('data', data)
        # ])
        #
        # return Response(data=Result.success(data=page_data))
