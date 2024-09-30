from django.db import models
from components.base_models import BaseModel


class UserInfo(BaseModel):
    id = models.AutoField(primary_key=True, help_text="自增主键")
    username = models.CharField(max_length=50, unique=True, help_text="用户名")
    name = models.CharField(max_length=50, null=True, default=None, help_text="姓名")
    email = models.CharField(max_length=50, null=True, default=None, help_text="邮箱")
    phone = models.CharField(max_length=50, null=True, default=None, help_text="联系电话")
    # status = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    # role = models.ForeignKey(to=Role, db_column='role_id', on_delete=models.CASCADE)
    orgs = models.CharField(max_length=500, null=True, default=None, help_text="组织架构")
    note = models.CharField(max_length=2000, blank=True, null=True, default=None, help_text="备注")
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
        return self.status

    # @property
    # def is_dba(self):
    #     return self.role == self.ROLE_ADMIN
    #

    def check_password(self, raw_password):
        return self.username


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
