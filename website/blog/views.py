import logging
from rest_framework import viewsets
from rest_framework import status
from blog import models
from blog import serializers
from components.pagination import TablePageNumberPagination, SizeTablePageNumberPagination
from components.response import ResultEnum


# from components.exceptions import BizException


# from website.blog import


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all().order_by('-create_time')
    serializer_class = serializers.ArticleSerializer
    pagination_class = SizeTablePageNumberPagination

    # def update(self, request, *args, **kwargs):
    #     print(request)
    #     # self.queryset.update_or_create()
    #     return super(ArticleViewSet, self).create(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     # raise BizException(ResultEnum.FAILURE)
    #     return super(ArticleViewSet, self).list(request)
