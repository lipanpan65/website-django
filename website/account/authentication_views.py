
import logging
from rest_framework import viewsets
from account.models import UserInfo
from account import serializers
from components.pagination import SizeTablePageNumberPagination
from components.response import ResultEnum, ApiResult


class AuthenticationViewSet(viewsets.ModelViewSet):
  queryset = UserInfo.objects.filter(enable=1,yn=1).all()
  
  @action(methods=["POST"], detail=False)
  def login(self,request,*args,**kwargs):
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
      response = Response({"code": 0, "msg": "SUCCESS", "data": data}, status=status.HTTP_200_OK)
      response.set_cookie("token", token.key, max_age=SESSION_COOKIE_AGE)
      response.set_cookie("username", user.username, max_age=SESSION_COOKIE_AGE)
      response.set_cookie("curRole", role.role_type, max_age=SESSION_COOKIE_AGE)
      return response
  else:
      data = dict(code=1, msg="用户登录失败", data=None)
      response = Response(data, status=status.HTTP_200_OK)
      return response

  @action(methods=["POST"], detail=False)
  def register(self,request,*args,**kwargs):
    """
    注册
    """
    username = request.data.get("username")
    # TODO 密码处理校验
    password = request.data.get("password")
    user = UserInfo.objects.save(**dict(user_name=user_name,password=password))
    if user:
      pass
    return ApiResult.success(data=user)
    

  
