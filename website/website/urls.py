"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from blog import views as blog_views

user_routers_v1 = DefaultRouter()

# #################### 用户路由配置 ####################### #

user_routers_v1.register(r'article', blog_views.ArticleViewSet, 'article')
user_routers_v1.register(r'article_category', blog_views.ArticleCategoryViewSet, 'article-category')
urlpatterns = [
    # path('admin/', admin.site.urls),
    # re_path(r'^api/user/v1/', include(user_routers_v1.urls, namespace='user_v1')),
    re_path(r'^api/user/v1/', include(user_routers_v1.urls)),
]
