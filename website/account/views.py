from django.shortcuts import render

# Create your views here.
import logging
from rest_framework import viewsets
from rest_framework import permissions
from account import models
from account import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from account.models import GlobalDict, Role
from components.pagination import SizeTablePageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
import uuid

from components.response import ResultEnum, ApiResult

logger = logging.getLogger()


class GlobalDictViewSet(viewsets.ModelViewSet):
    queryset = GlobalDict.objects.all()
    serializer_class = serializers.GlobalDictSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('cname', 'ckey')
    filterset_fields = ('enable',)

    # ordering_fields = ('id',)

    def create(self, request, *args, **kwargs):
        request.data.update({
            "create_user": request.user.username,
            "update_user": request.user.username
        })
        return super().create(request, args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data.update({
            "create_user": request.user.username,
            "update_user": request.user.username
        })
        return super(GlobalDictViewSet, self).update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     pass

    @action(methods=["GET"], detail=False)
    def validate_cname(self, request, *args, **kwargs):
        """
        校验名称是否存在
        """
        cname = request.query_params.get("cname")
        queryset = self.queryset.filter(cname=cname)
        exists = queryset.exists()
        data = dict(exists=exists, code=0)
        return Response(status=status.HTTP_200_OK, data=data)

    @action(methods=["GET"], detail=False)
    def validate_ctype(self, request, *args, **kwargs):
        """
        校验ctype
        """
        ctype = request.query_params.get("ctype")
        queryset = self.queryset.filter(ctype=ctype)
        exists = queryset.exists()
        data = dict(exists=exists, code=0)
        return Response(status=status.HTTP_200_OK, data=data)


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all().order_by('-create_time')
    serializer_class = serializers.UserInfoSerializer
    pagination_class = SizeTablePageNumberPagination
    permission_classes = [permissions.AllowAny]

    filterset_fields = ('enable',)

    def create(self, request, *args, **kwargs):
        data = request.data
        role_id = data.get('role_id')
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
                request.data['role_name'] = role.role_name
            except Role.DoesNotExist:
                return ApiResult.failure()

        # org_id = data.get('org_id')
        # if org_id:
        #     try:
        #         org = models.Organizations.objects.get(org_id=org_id)
        #         # request.data['org_fullname'] = org.org_fullname
        #     except models.Organizations.DoesNotExist:
        #         return ApiResult.failure()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return super(UserInfoViewSet, self).create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('-create_time')
    serializer_class = serializers.RoleSerializer
    pagination_class = SizeTablePageNumberPagination
    filterset_fields = ('enable', 'role_type')


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


class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = models.Organizations.objects.all().order_by('-create_time')
    serializer_class = serializers.OrganizationTreeSerializer
    pagination_class = SizeTablePageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(parent_org_id__isnull=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        创建组织架构
        """
        org_id = str(uuid.uuid4())  # 自定义 org_id
        parent_org_id = request.data.get('parent_org_id')
        org_name = request.data.get('org_name')

        if parent_org_id is None:
            # 如果没有父组织ID，说明是根组织，全称就是自身名称
            org_fullname = org_name
        else:
            try:
                # 获取父组织实例
                parent_org = models.Organizations.objects.get(org_id=parent_org_id)
                # 生成组织架构全称
                org_fullname = f"{parent_org.get_full_org_name()}-{org_name}"
            except models.Organizations.DoesNotExist:
                return Response({"error": "父组织不存在"}, status=status.HTTP_400_BAD_REQUEST)

        request.data.update({"org_id": org_id, "org_fullname": org_fullname})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except models.Organizations.DoesNotExist:
            return ApiResult.failure()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 自动更新 org_fullname（仅当 org_name 或 parent_org_id 变化时）
        if 'org_name' in serializer.validated_data or 'parent_org_id' in serializer.validated_data:
            serializer.validated_data['org_fullname'] = instance.get_full_org_name()
        # 保存并返回
        serializer.save()
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return ApiResult.success()
        # return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            children = instance.get_sub_children()
            if children:
                # 使用 for 循环删除每个子节点
                for child in children:
                    child.delete()
            # 删除当前节点
            self.perform_destroy(instance)
            # return Response(status=status.HTTP_204_NO_CONTENT)
            return ApiResult.success()
        except Exception as e:
            # 处理异常，返回错误信息
            # return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return ApiResult.failure(detail=str(e))
