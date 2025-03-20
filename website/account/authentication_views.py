import logging
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import login as origin_login
from django.contrib.auth import logout as origin_logout
from account.models import UserInfo, Token
# from rest_framework.authtoken.models import Token
from account import serializers
from components.pagination import SizeTablePageNumberPagination
from components.response import ResultEnum, ApiResult

SESSION_COOKIE_AGE = getattr(settings, 'SESSION_COOKIE_AGE')  # 默认24小时


class AuthenticationViewSet(viewsets.ModelViewSet):
    # queryset = UserInfo.objects.filter(enable=1, yn=1).all()
    queryset = UserInfo.objects.all()
    permission_classes = [AllowAny]

    @action(methods=["POST"], detail=False)
    def logout(self, request, *args, **kwargs):
        """ 用户登出 """
        if request.user.id:
            Token.objects.filter(user=request.user).delete()
        request.session.flush()
        data = dict(code=0, msg="SUCCESS", data=dict(usename=None, name=None, role=None, token=None))
        response = Response(data, status=status.HTTP_200_OK)
        origin_logout(request)
        response.delete_cookie('token')
        response.delete_cookie('username')
        response.delete_cookie('curRole')
        return response

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        """
        用户登录
        """
        username = request.data.get("username")
        # TODO 密码处理校验
        password = request.data.get("password")
        user = self.queryset.filter(username=username).first()
        if user and user.is_active:
            if request.user != user:
                origin_login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            role = user.role
            data = dict(username=user.username, name=user.name, role=role.role_type, token=token.key)
            response = ApiResult.success(data=data)
            # response = Response({"code": 0, "msg": "SUCCESS", "data": data}, status=status.HTTP_200_OK)
            response.set_cookie("token", token.key, max_age=SESSION_COOKIE_AGE)
            response.set_cookie("username", user.username, max_age=SESSION_COOKIE_AGE)
            # response.set_cookie("curRole", role.role_type, max_age=SESSION_COOKIE_AGE)
            return response
        else:
            response = ApiResult.failure(message="用户登陆失败")
            # data = dict(code=1, msg="用户登录失败", data=None)
            # response = Response(data, status=status.HTTP_200_OK)
            return response

    @action(methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        """
        注册
        """
        username = request.data.get("username")
        # TODO 密码处理校验
        password = request.data.get("password")
        user = UserInfo.objects.save(**dict(user_name=user_name, password=password))
        # UserInfo.objects.create(user=user)
        if user:
            pass
        return ApiResult.success(data=user)
