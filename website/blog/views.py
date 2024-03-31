import logging
from rest_framework import viewsets
from rest_framework import status
from blog import models
from blog import serializers
from components.pagination import TablePageNumberPagination, SizeTablePageNumberPagination
from components.response import ResultEnum, ApiResult


# from components.exceptions import BizException


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
    #     raise ValueError('this is test')
    #     return super(ArticleViewSet, self).list(request)

    def publish(self, request, *args, **kwargs):
        """
        发布文章
        """
        pass
        return ApiResult.success()


class ArticleCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.ArticleCategory.objects.all().order_by('-create_time')
    serializer_class = serializers.ArticleCategorySerializer
    pagination_class = SizeTablePageNumberPagination
