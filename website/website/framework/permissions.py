import re
from rest_framework.permissions import BasePermission


class UserRolePermission(BasePermission):
    PATTERN_LOGIN_API = re.compile(r'^/api/operation/configure/user/login/')
    PATTERN_LOGOUT_API = re.compile(r'^/api/operation/configure/user/logout/')
    PATTERN_API = re.compile(r'^/api/v\d+\.\d+/')
    PATTERN_API_V1 = re.compile(r'^/api/v1\.\d+/')
    PATTERN_API_V2 = re.compile(r'^/api/v2\.\d+/')
    PATTERN_COMMON = re.compile(r'^/api/common/')
    PATTERN_WEIXIN = re.compile(r'^/api/weixin/')

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print(request.user)
        return True
