import logging
from rest_framework import viewsets

from blog import models
from blog import serializers
from components.pagination import TablePageNumberPagination


# from website.blog import


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all().order_by('-create_time')
    serializer_class = serializers.ArticleSerializer
    pagination_class = TablePageNumberPagination

    # def update(self, request, *args, **kwargs):
    #     print(request)
    #     # self.queryset.update_or_create()
    #     return super(ArticleViewSet, self).create(request, *args, **kwargs)
