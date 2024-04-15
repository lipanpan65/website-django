import logging
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from blog import models
from blog import serializers
from components.pagination import TablePageNumberPagination, SizeTablePageNumberPagination
from components.response import ResultEnum, ApiResult

logger = logging.getLogger()


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

    @action(methods=['POST'], detail=False)
    def publish(self, request, *args, **kwargs):
        """
        发布文章
        """
        instance = self.get_object()

        return ApiResult.success()


class ArticleCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.ArticleCategory.objects.all().order_by('-create_time')
    serializer_class = serializers.ArticleCategorySerializer
    pagination_class = SizeTablePageNumberPagination

    @action(methods=['GET'], detail=False)
    def validate_category_name(self, request, *args, **kwargs):
        """
        校验名称是否存在
        """
        # logger.info("[校验分类名称是否存在] %s" % request)
        logger.info("[校验分类名称是否存在] %s" % dir(request))
        logger.info("[校验分类名称是否存在] %s" % request.query_params)
        category_name = request.query_params.get('category_name')
        # TODO 校验字符串是否为空
        queryset = self.queryset.filter(category_name=category_name)
        if queryset.exists():
            message = '分类名称：%s 已经存在' % category_name
            return ApiResult.failure(message=message, data=queryset.values())
        return ApiResult.success()
