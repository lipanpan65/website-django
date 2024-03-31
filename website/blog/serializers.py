from rest_framework import serializers
from blog import models


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleCategory
        fields = '__all__'
