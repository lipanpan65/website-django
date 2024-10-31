from django.db import models
from components.base_models import BaseModel


class UserInfo(BaseModel):
    STATUS = ()
    STATUS_ENABLE = ""
    id = models.AutoField(primary_key=True, help_text="自增主键")
    username = models.CharField(max_length=50, unique=True, help_text="用户名")
    name = models.CharField(max_length=50, null=True, default=None, help_text="姓名")
    email = models.CharField(max_length=50, null=True, default=None, help_text="邮箱")
    phone = models.CharField(max_length=50, null=True, default=None, help_text="联系电话")
    enable = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    # role = models.ForeignKey(to=Role, db_column='role_id', on_delete=models.CASCADE)
    orgs = models.CharField(max_length=500, null=True, default=None, help_text="组织架构")
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


class Role(models.Model):
    STATUS_DISABLE = 0
    STATUS_ENABLE = 1

    ROLE_RD = 0
    ROLE_ADMIN = 1
    ROLE_TYPE = (
        (ROLE_RD, "普通用户"),
        (ROLE_ADMIN, "管理员")
    )

    STATUS = (
        (STATUS_ENABLE, "启用"),
        (STATUS_DISABLE, "禁用")
    )

    id = models.AutoField(primary_key=True, help_text="自增主键")
    name = models.CharField(max_length=128, help_text='角色名称')
    # role_type = models.CharField(max_length=128, help_text='角色类型:user 普通用户 admin 管理员')
    # role_key = models.CharField(max_length=128, help_text="角色唯一标识")
    role_type = models.IntegerField(choices=ROLE_TYPE, default=1, null=True, help_text="管理员类型：管理员、开发管理员")
    status = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    create_user = models.CharField(max_length=128, default=None, help_text='创建人')
    update_user = models.CharField(max_length=128, default=None, help_text='修改人')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='修改时间')
    remark = models.CharField(max_length=200, default=None, help_text='备注')

    # users = models.ManyToManyField(UserInfo, through='User2Role', through_fields=('user', 'role'), blank=True,
    #                                related_name='role_user')
    class Meta:
        db_table = "dbms_user_role"


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
        children = self.children
        sub_children = list(children)
        if not sub_children:
            return sub_children
        for child in children:
            sub_children.extend(child.get_sub_children())
        return sub_children

    # class User2Role(models.Model):


#     id = models.AutoField(primary_key=True, help_text="自增主键")
#     user = models.ForeignKey(to=UserInfo, db_column='user_id', on_delete=models.CASCADE)
#     role = models.ForeignKey(to=Role, db_column='role_id', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "dbms_user2role"


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


"""
CREATE TABLE `dbms_user2role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `user_name` 
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  `role_name` 
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_role` (`user_id`,`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基础信息表-用户角色关联表';

"""

"""
CREATE TABLE `dbms_global_dict` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cname` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典名称',
  `ckey` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典Key：唯一且不能修改',
  `cvalue` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典的Value',
  `enable` smallint NOT NULL DEFAULT '1' COMMENT '状态：1:启用，0:禁用',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_user` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '创建人',
  `update_user` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '更新人',
  `remakr` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `yn` tinyint DEFAULT '1' COMMENT '是否有效:1有效,0无效',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_ckey` (`ckey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='基础信息表-全局字典'

"""


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
    # create_user = models.CharField(max_length=50, help_text='创建人', default=None)
    # update_user = models.CharField(max_length=50, help_text='修改人', null=True)
    remark = models.CharField(max_length=256, help_text="备注", null=True, blank=True)
    yn = models.SmallIntegerField(default=1, help_text='是否有效:1有效,0无效')

    class Meta:
        db_table = 'dbms_global_dict'
