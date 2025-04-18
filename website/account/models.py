import binascii
import os

from django.db import models
from django.db.models import Prefetch
from components.base_models import BaseModel
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Organizations(models.Model):
    ORGANIZATION_TYPES = [
        ('company', '公司'),
        ('department', '部门'),
        ('branch', '分公司'),
        ('business_unit', '业务单元'),
        ('team', '团队'),
        ('project_team', '项目组'),
        ('regional_office', '区域分部'),
        ('functional_center', '职能中心'),
        ('virtual_team', '虚拟组织'),
    ]

    # 自增主键，自动生成唯一ID
    id = models.AutoField(primary_key=True, help_text="自增主键，唯一标识")
    # 组织架构的唯一ID，字符类型，最大长度30
    org_id = models.CharField(max_length=255, unique=True, help_text="组织架构ID，用于唯一标识组织")
    # 组织架构名称，字符类型，最大长度255
    org_name = models.CharField(max_length=255, help_text="组织架构名称")
    # 父组织ID，用于层级结构表示，可为空
    parent_org_id = models.CharField(max_length=255, blank=True, null=True, help_text="父组织ID，顶级组织为空")
    # 启用状态，默认1为启用，0为禁用
    enable = models.IntegerField(default=1, help_text="启用状态，1表示启用，0表示禁用")
    # 组织架构全称，字符类型，最大长度255
    org_fullname = models.CharField(max_length=255, help_text="组织架构全名")
    # 组织层级，表示组织在层级结构中的深度
    org_level = models.IntegerField(default=1, help_text="组织层级，从顶层开始递增")
    # 备注信息，用于描述组织的额外信息
    remark = models.TextField(blank=True, null=True, help_text="备注信息，描述组织的附加说明")
    # 记录创建时间，默认当前时间
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    # 记录更新时间，默认当前时间
    update_time = models.DateTimeField(auto_now=True, help_text="更新时间")
    # 组织类型，使用预定义的枚举值（如公司、部门、团队等）
    org_type = models.CharField(
        max_length=50,
        choices=ORGANIZATION_TYPES,
        help_text="组织类型，例如：公司、部门、团队等",
        default='company'
    )
    # 组织的负责人ID，指向用户ID，可为空
    manager_id = models.IntegerField(null=True, blank=True, help_text="组织负责人ID")

    # 显示顺序，用于定义展示的排序，默认值为0
    sort_order = models.IntegerField(default=0, help_text="显示顺序")

    # 逻辑删除标志，1表示有效，0表示无效（软删除）
    yn = models.BooleanField(default=True, help_text="逻辑删除标志，1为有效，0为无效")

    class Meta:
        db_table = 'dbms_organizations'
        verbose_name = '组织架构'
        verbose_name_plural = '组织架构'

    def __str__(self):
        return f"{self.org_name} ({self.org_id})"

    def save(self, *args, **kwargs):
        # 自动计算完整名称
        self.org_fullname = self.get_full_org_name()
        super().save(*args, **kwargs)

    @classmethod
    def parents(cls):
        """
        获取全量的父级菜单
        """
        return cls.objects.filter(parent_org_id__isnull=True)

    @property
    def children(self):
        """ 获取当前菜单的全部子菜单 """
        queryset = Organizations.objects.filter(parent_org_id=self.org_id).all()
        return queryset if queryset else []

    def get_sub_children(self):
        """
        获取所有的子节点
        """
        # 用于记录已经访问过的节点，避免循环引用
        visited = set()
        sub_children = []

        def _get_children(node):
            nonlocal sub_children
            if node.org_id in visited:
                return
            visited.add(node.org_id)
            children = node.children
            sub_children.extend(children)
            for child in children:
                _get_children(child)

        _get_children(self)
        return sub_children

    def get_sub_children_v2(self):
        """
        获取所有的子节点
        """
        # 用于记录已经访问过的节点，避免循环引用
        visited = set()
        sub_children = []

        def _get_children(node):
            nonlocal sub_children
            if node.org_id in visited:
                return
            visited.add(node.org_id)
            # 使用 prefetch_related 一次性获取子节点
            children = node.children.prefetch_related(Prefetch('children'))
            sub_children.extend(children)
            for child in children:
                _get_children(child)

        _get_children(self)
        return sub_children

    def get_full_org_name(self):
        """
        递归获取当前节点的全部父节点，并使用 - 连接它们的名称
        """
        names = [self.org_name]
        parent = self.get_parent()
        while parent:
            names.insert(0, parent.org_name)
            parent = parent.get_parent()
        return "-".join(names)

    def get_parent(self):
        """
        获取当前节点的父节点
        """
        if self.parent_org_id:
            try:
                return Organizations.objects.get(org_id=self.parent_org_id)
            except Organizations.DoesNotExist:
                return None
        return None


class Permission(BaseModel):
    id = models.BigAutoField(primary_key=True)
    permission_name = models.CharField(max_length=100, unique=True, verbose_name='权限名称')
    permission_code = models.CharField(max_length=100, unique=True, verbose_name='权限代码（如 user:create）')
    category = models.CharField(max_length=50, verbose_name='权限类别（如 user, order, product）')
    enable = models.SmallIntegerField(default=1, help_text='状态：1:启用，0:禁用')
    parent_permission = models.ForeignKey(to="self", on_delete=models.SET_NULL, related_name='child_permissions',
                                          null=True, blank=True)
    create_user = models.CharField(max_length=50, verbose_name='创建人用户名', null=True, default="lipanpan65", )
    update_user = models.CharField(max_length=50, null=True, blank=True, verbose_name='更新人用户名',
                                   default="lipanpan65", )
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name='权限备注')
    yn = models.BooleanField(default=True, verbose_name='是否有效（1=有效, 0=无效）')

    class Meta:
        db_table = 'dbms_permissions'
        verbose_name = '权限'
        verbose_name_plural = '权限'

    @classmethod
    def parents(cls):
        """
        获取全量的父级菜单
        """
        return cls.objects.filter(parent_permission_id__isnull=True)

    @property
    def children(self):
        """ 获取当前菜单的全部子菜单 """
        queryset = Permission.objects.filter(parent_permission=self.id).all()
        return queryset if queryset else []

    def get_sub_children(self):
        """
        获取所有的子节点
        """
        # 用于记录已经访问过的节点，避免循环引用
        visited = set()
        sub_children = []

        def _get_children(node):
            nonlocal sub_children
            if node.id in visited:
                return
            visited.add(node.id)
            children = node.children
            sub_children.extend(children)
            for child in children:
                _get_children(child)

        _get_children(self)
        return sub_children


class Role(BaseModel):
    STATUS_DISABLE = 0
    STATUS_ENABLE = 1

    ROLE_RD = 0
    ROLE_ADMIN = 1
    ROLE_SUPER_ADMIN = 2
    ROLE_TYPE = (
        (ROLE_RD, "普通用户"),
        (ROLE_ADMIN, "管理员"),
        (ROLE_SUPER_ADMIN, "超级管理员")
    )

    STATUS = (
        (STATUS_ENABLE, "启用"),
        (STATUS_DISABLE, "禁用")
    )

    id = models.AutoField(primary_key=True, help_text="自增主键")
    role_name = models.CharField(max_length=128, help_text='角色名称')
    role_type = models.SmallIntegerField(choices=ROLE_TYPE, default=1, null=True,
                                         help_text="管理员类型：管理员、开发管理员")
    enable = models.SmallIntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    create_user = models.CharField(max_length=128, default=None, help_text='创建人')
    update_user = models.CharField(max_length=128, default=None, help_text='修改人')
    remark = models.CharField(max_length=200, default=None, help_text='备注')
    yn = models.SmallIntegerField(default=1, help_text='是否有效:1有效,0无效')

    # users = models.ManyToManyField(UserInfo, through='User2Role', through_fields=('user', 'role'), blank=True,
    #                                related_name='role_user')
    permissions = models.ManyToManyField(Permission,
                                         through='Role2Permission',
                                         through_fields=('role', 'permission'),
                                         blank=True,
                                         related_name='roles')

    class Meta:
        db_table = "dbms_user_role"


class UserInfo(BaseModel, AbstractBaseUser):
    STATUS_DISABLE = 0
    STATUS_ENABLE = 1

    STATUS = (
        (STATUS_ENABLE, "启用"),
        (STATUS_DISABLE, "禁用")
    )

    id = models.AutoField(primary_key=True, help_text="自增主键")
    username = models.CharField(max_length=50, unique=True, help_text="用户名")
    password = models.CharField(max_length=255, help_text='用户密码')
    name = models.CharField(max_length=50, null=True, default=None, help_text="姓名")
    email = models.CharField(max_length=50, null=True, default=None, help_text="邮箱")
    phone = models.CharField(max_length=50, null=True, default=None, help_text="联系电话")
    enable = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    role_id = models.ForeignKey(to=Role, db_column='role_id', on_delete=models.CASCADE)
    role_type = models.SmallIntegerField(choices=Role.ROLE_TYPE, default=1, null=True,
                                         help_text="管理员类型：管理员、开发管理员")
    org_id = models.ForeignKey(to=Organizations, db_column='org_id', to_field='org_id', on_delete=models.CASCADE)
    remark = models.CharField(max_length=2000, blank=True, null=True, default=None, help_text="备注")
    create_user = models.CharField(max_length=100, null=True, default="lipanpan65", help_text="创建人")
    update_user = models.CharField(max_length=100, null=True, default="lipanpan65", help_text="更新人")
    last_login = None
    backend = 'django.contrib.auth.backends.ModelBackend'
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    _bsp_user = None

    class Meta:
        db_table = "dbms_userinfo"
        # auto_created = True

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    @classmethod
    def get_user(cls, username, *args, **kwargs):
        """ 根据用户名获取用户 """
        user = cls.objects.filter(username=username)
        if user.exists():
            return True, user
        else:
            return False, None

    # def natural_key(self):
    #     return (self.get_username(),)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return self.username

    @property
    def is_active(self):
        return self.enable

    # @property
    # def is_dba(self):
    #     return self.role == self.ROLE_ADMIN
    #

    def check_password(self, raw_password):
        return self.username


# class RoleViewSet(viewsets.ModelViewSet):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#
#     def create(self, request, *args, **kwargs):
#         username = request.user.username
#         request.data.update(dict(create_user=username, update_user=username))
#         return super().create(request, *args, **kwargs)
#
#     @action(methods=["GET"], detail=False)
#     def validate_name(self, request, *args, **kwargs):
#         """
#         校验名称是否存在,并且唯一
#         创建的时候 数据不存在 且 count 为 0
#         更新 数据存在 且 count 为 1
#         """
#         data = dict(exists=True, code=0)
#         id = self.request.query_params.get("id", 0)
#         name = self.request.query_params.get("name")
#         queryset = self.queryset.filter(name=name)
#         exists, count = queryset.exists(), queryset.count()
#         if not exists:  # 如果不存在,则校验直接通过 对应创建操作
#             data = dict(exists=exists, code=0)
#         else:  # 如果存在,则判断是否操作的为同一对象,如果是 则直接通过校验
#             if int(id) == queryset.first().id:
#                 data = dict(exists=False, code=0)
#         return Response(status=status.HTTP_200_OK, data=data)


class Menus(BaseModel):
    STATUS_DISABLE = 0
    STATUS_ENABLE = 1

    STATUS = (
        (STATUS_ENABLE, "启用"),
        (STATUS_DISABLE, "禁用")
    )

    id = models.AutoField(primary_key=True, help_text="自增主键")
    menu_name = models.CharField(max_length=64, help_text='菜单名称')
    enable = models.SmallIntegerField(default=1, help_text='状态：1:启用，0:禁用')
    url = models.CharField(max_length=255, help_text='URL')
    icon = models.CharField(max_length=255, default='', help_text='菜单图标')
    menu_type = models.IntegerField(default=1, help_text='菜单1,按钮2,目录0')
    element = models.CharField(max_length=255, null=True, help_text='组件名称')
    # status = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    # hidden = models.IntegerField(default=1, help_text='1:显示,0:隐藏')
    # linked = models.IntegerField(default=0, help_text='1外链,0非外链')
    pid = models.ForeignKey("self", db_column='pid', on_delete=models.CASCADE, null=True, default=None,
                            help_text="主键自增")
    remark = models.CharField(max_length=255, default=None, help_text='备注')
    yn = models.SmallIntegerField(default=1, help_text='是否有效:1有效,0无效')

    class Meta:
        db_table = "dbms_menus"

    def to_dict(self):
        """
        将 object 转为 dict
        """
        obj_dict = self.__dict__
        return {key: value for key, value in obj_dict.items() if not key.startswith('_')}

    @property
    def parent(self):
        return Menus.objects.filter(id=self.pid).first()

    @property
    def branches(self):
        """
        返回当前节点到跟节点的全部节点
        """
        sub_branches = [self]
        while True:
            # 获取最后一个节点
            parent = sub_branches[-1].parent
            if not parent:
                break
            sub_branches.append(parent)
        # 倒叙
        return sub_branches[::-1]

    @classmethod
    def parents(cls):
        """
        获取全量的父级菜单
        """
        return cls.objects.filter(pid__isnull=True)

    @property
    def children(self):
        """ 获取当前菜单的全部子菜单 """
        queryset = Menus.objects.filter(pid=self.id).all()
        return queryset if queryset else []

    def get_sub_children(self):
        """
        获取所有的子节点
        """
        # 用于记录已经访问过的节点，避免循环引用
        visited = set()
        sub_children = []

        def _get_children(node):
            nonlocal sub_children
            if node.org_id in visited:
                return
            visited.add(node.org_id)
            children = node.children
            sub_children.extend(children)
            for child in children:
                _get_children(child)

        _get_children(self)
        return sub_children

    # def get_sub_children(self):
    #     """
    #     获取所有的子节点
    #     """
    #     children = self.children
    #     sub_children = list(children)
    #     if not sub_children:
    #         return sub_children
    #     for child in children:
    #         sub_children.extend(child.get_sub_children())
    #     return sub_children

    # class User2Role(models.Model):


class User2Role(models.Model):
    id = models.AutoField(primary_key=True, help_text="自增主键")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id', verbose_name='用户ID')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id', verbose_name='角色ID')

    class Meta:
        db_table = 'dbms_user2role'
        verbose_name = '基础信息表-用户角色关联表'
        unique_together = ('user', 'role')

    def __str__(self):
        return f"User {self.user_id} - Role {self.role_id}"


# class UserGroup(models.Model):
#     id = models.AutoField(primary_key=True, help_text="自增主键")
#     name = models.CharField(max_length=128, help_text='角色名称')
#     create_time = models.DateTimeField(auto_now=True, help_text="创建时间")
#     create_user = models.CharField(max_length=100, null=True, help_text="创建人")
#     update_time = models.DateTimeField(auto_now=True, help_text="更新时间")
#     update_user = models.CharField(max_length=100, null=True, help_text="更新人")
#     note = models.CharField(max_length=2000, blank=True, null=True, help_text="备注")
#     users = models.ManyToManyField(UserInfo,
#                                    through='User2Group',
#                                    through_fields=('group', 'user',),
#                                    blank=True,
#                                    related_name='user_group', )

# models.ManyToManyRel
# class Meta:
#     db_table = "dbms_user_group"

# def add_user(self, username, *args, **kwargs):
# username = kwargs.get("username")
# exists, user = UserInfo.get_user(username=username)
# if exists:
#     User2Group.objects.create(user=user.first(), group=self)


class OrganizationRelation(models.Model):
    parent_org_id = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='child_relations'
    )
    org_id = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='parent_relations'
    )

    class Meta:
        abstract = True
        managed = False


class GlobalDict(BaseModel):
    """
    全局字典表
    """
    id = models.AutoField('id', primary_key=True, help_text='自增主键')
    cname = models.CharField(max_length=100, help_text="名称")
    # ctype = models.CharField(max_length=50, help_text='类型')  # 修改字段名称
    ckey = models.CharField(max_length=128, help_text='key值')
    cvalue = models.TextField(help_text='value值')
    enable = models.IntegerField(help_text='状态: [在用]1 [禁用]0', default=1)
    remark = models.CharField(max_length=256, help_text="备注", null=True, blank=True)
    yn = models.SmallIntegerField(default=1, help_text='是否有效:1有效,0无效')

    class Meta:
        db_table = 'dbms_global_dict'

    @classmethod
    def get(cls, item):
        try:
            obj = cls.objects.get(ckey=item)
            return obj.cvalue
        except cls.DoesNotExist:
            return None

    @classmethod
    def __fetch(cls, type, key):
        return cls.objects.filter(ctype=type, ckey=key, status=1).first()

    @classmethod
    def __array(cls, type, key):
        return [v.strip() for v in cls.__fetch(type, key).cvalue.split(',')]

    @classmethod
    def __int(cls, type, key):
        return int(cls.__fetch(type, key).cvalue)

    @classmethod
    def __bool(cls, type, key):
        return bool(cls.__int(type, key))


"""
class Organizations(models.Model):
    # 原有字段保持不变...

    @classmethod
    def parents(cls):

        # 获取全量的父级菜单
        return cls.objects.filter(parent_org_id__isnull=True)

    # 将 @property 方法替换为反向关联字段
    children = models.ManyToManyField(
        'self',
        related_name='parent_organizations',
        symmetrical=False,
        through_fields=('parent_org_id', 'org_id'),
        through='OrganizationRelation'
    )

    def get_sub_children(self):
        # 获取所有的子节点
        # 用于记录已经访问过的节点，避免循环引用
        visited = set()
        sub_children = []

        def _get_children(node):
            nonlocal sub_children
            if node.org_id in visited:
                return
            visited.add(node.org_id)
            # 使用 prefetch_related 一次性获取子节点
            children = node.children.prefetch_related('children')
            sub_children.extend(children)
            for child in children:
                _get_children(child)

        _get_children(self)
        return sub_children

class OrganizationRelation(models.Model):
    parent_org_id = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='child_relations'
    )
    org_id = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='parent_relations'
    )
    class Meta:
        managed = False

"""


class Role2Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(to=Role, on_delete=models.SET_NULL, db_column='role_id',
                             related_name='role2_permissions', null=True)
    permission = models.ForeignKey(to=Permission, on_delete=models.SET_NULL, db_column='permission_id',
                                   related_name='role2_permissions', null=True)

    class Meta:
        # managed = False
        db_table = 'dbms_role2permission'
