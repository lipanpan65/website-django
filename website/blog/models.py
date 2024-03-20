from django.db import models
from components.base_models import BaseModel


class Article(BaseModel):
    ARTICLE_STATUS = (
        ('draft', u'草稿'),
        ('publish', u'已发布')
    )

    id = models.AutoField(db_column='id', primary_key=True, verbose_name='自增主键')
    status = models.CharField(db_column='status', max_length=64, choices=ARTICLE_STATUS, default='draft',
                              verbose_name='帖子状态')
    title = models.CharField(db_column='title', max_length=256, null=True, default='无标题', blank=True,
                             verbose_name='标题')
    content = models.TextField(db_column='content', default=None, null=True, blank=True, verbose_name='帖子内容')
    content_html = models.TextField(db_column='content_html', default=None, blank=True, null=True,
                                    verbose_name='帖子内容html')
    create_user = models.CharField(db_column='create_user', max_length=256, null=True, default=None,
                                   verbose_name='添加人')
    update_user = models.CharField(db_column='update_user', max_length=256, null=True, default=None,
                                   verbose_name='修改人')

    # create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_blog_article'


class ArticleCategory(BaseModel):
    id = models.AutoField(db_column='id', primary_key=True, help_text='自增主键')
    category_name = models.CharField(db_column='category_name', max_length=256, help_text='分类名称')
    create_user = models.CharField(db_column='create_user', max_length=256, null=True, default=None, help_text='添加人')
    update_user = models.CharField(db_column='update_user', max_length=256, null=True, default=None, help_text='修改人')
    yn = models.SmallIntegerField(default=1, help_text='数据是否有效')

    class Meta:
        db_table = 'tb_article_category'
