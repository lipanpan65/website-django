from django.shortcuts import render

# Create your views here.
import logging
from rest_framework import viewsets
from account import models
from account import serializers
from components.pagination import SizeTablePageNumberPagination
from components.response import ResultEnum, ApiResult

logger = logging.getLogger()


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menus.objects.all().order_by('-create_time')
    # serializer_class = serializers.MenusSerializer
    serializer_class = serializers.MenusTreeSerializer
    pagination_class = SizeTablePageNumberPagination

    # def get_queryset(self):
    #     queryset = self.filter_queryset(self.queryset)
    #     queryset = queryset.filter(pid__isnull=True)
    #     return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(pid__isnull=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        children = instance.get_sub_children()
        if children:
            map(lambda child: child.delete(), children)
            # children.delete()
        return super().destroy(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     data = []
    #     queryset = self.filter_queryset(self.get_queryset())
    #     parents = queryset.filter(pid__isnull=True)
    #     # for parent in parents:
    #     #     children_dict = []
    #     #     children = parent.get_sub_children()
    #     #     logger.info('children:%s' % children)
    #     #     # parent_dict = parent.__dict__
    #     #     # parent = {key: value for key, value in parent_dict.items() if not key.startswith('_')}
    #     #     parent = parent.to_dict()
    #     #     for child in children:
    #     #         children_dict.append(child.to_dict())
    #     #     parent.update(children=children_dict)
    #     #     data.append(parent)
    #
    #     page = self.paginate_queryset(parents)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         serializer = serializers.MenusTreeSerializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #         # return self.get_paginated_response(data)
    #
    #     serializer = self.get_serializer(data, many=True)
    #     return ApiResult.success(data=serializer.data)
