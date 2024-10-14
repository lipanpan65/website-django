from rest_framework.permissions import BasePermission
from account.models import UserInfo

class UserRolePermission(BasePermission):
    PATTERN_PASSPORT_API = re.compile(r'^/api/operation/configure/user/login/')
    PATTERN_API = re.compile(r'^/api/v\d+\.\d+/')
    PATTERN_API_V1 = re.compile(r'^/api/v1\.\d+/')
    PATTERN_API_V2 = re.compile(r'^/api/v2\.\d+/')
    PATTERN_COMMON = re.compile(r'^/api/common/')
    PATTERN_WEIXIN = re.compile(r'^/api/weixin/')

    def has_permission(self, request, view):
    """
    Return `True` if permission is granted, `False` otherwise.
    """
    path = request.path
    if PATTERN_PASSPORT_API.match(path):
        return True
    
    # 如果用户为系统管理员则返回True,否则返回False
    is_admin = (isinstance(request.user, UserInfo) and request.user.role.role_type == 1)
    if not is_admin:
        return False

    return True




