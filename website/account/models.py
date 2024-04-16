from django.db import models
from components.base_models import BaseModel

class UserInfo(BaseModel):
    id = models.AutoField(primary_key=True, help_text="自增主键")
    username = models.CharField(max_length=50, unique=True, help_text="用户名")
    name = models.CharField(max_length=50, null=True, default=None, help_text="姓名")
    email = models.CharField(max_length=50, null=True, default=None, help_text="邮箱")
    phone = models.CharField(max_length=50, null=True, default=None, help_text="联系电话")
    status = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    role = models.ForeignKey(to=Role, db_column='role_id', on_delete=models.CASCADE)
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

    @property
    def is_dba(self):
        return self.role == self.ROLE_ADMIN

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
    name = models.CharField(max_length=128, help_text='菜单名称')
    url = models.CharField(max_length=255, help_text='URL')
    menu_type = models.IntegerField(default=1, help_text='菜单1,按钮2,目录0')
    icon = models.CharField(max_length=255, help_text='菜单图标')
    status = models.IntegerField(choices=STATUS, default=STATUS_ENABLE, help_text="状态：1为在用，0为禁用")
    element = models.CharField(max_length=255, null=True, help_text='组件名称')
    hidden = models.IntegerField(default=1, help_text='1:显示,0:隐藏')
    linked = models.IntegerField(default=0, help_text='1外链,0非外链')
    note = models.CharField(max_length=200, default=None, help_text='备注')
    pid = models.ForeignKey("self", db_column='pid', on_delete=models.CASCADE, null=True, default=None,
                            help_text="主键自增")



class User2Role(models.Model):
    id = models.AutoField(primary_key=True, help_text="自增主键")
    user = models.ForeignKey(to=UserInfo, db_column='user_id', on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, db_column='role_id', on_delete=models.CASCADE)

    class Meta:
        db_table = "dbms_user2role"


class UserGroup(models.Model):
    id = models.AutoField(primary_key=True, help_text="自增主键")
    name = models.CharField(max_length=128, help_text='角色名称')
    create_time = models.DateTimeField(auto_now=True, help_text="创建时间")
    create_user = models.CharField(max_length=100, null=True, help_text="创建人")
    update_time = models.DateTimeField(auto_now=True, help_text="更新时间")
    update_user = models.CharField(max_length=100, null=True, help_text="更新人")
    note = models.CharField(max_length=2000, blank=True, null=True, help_text="备注")
    users = models.ManyToManyField(UserInfo,
                                   through='User2Group',
                                   through_fields=('group', 'user',),
                                   blank=True,
                                   related_name='user_group', )

    # models.ManyToManyRel
    class Meta:
        db_table = "dbms_user_group"

    def add_user(self, username, *args, **kwargs):
        # username = kwargs.get("username")
        exists, user = UserInfo.get_user(username=username)
        if exists:
            User2Group.objects.create(user=user.first(), group=self)