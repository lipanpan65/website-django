# -*- coding: utf-8 -*-
# @Time        : 2024/4/9
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : serializers.py
from rest_framework import serializers
from account import models


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menus
        fields = '__all__'
