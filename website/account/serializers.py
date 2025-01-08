# -*- coding: utf-8 -*-
# @Time        : 2024/4/9
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : serializers.py
from rest_framework import serializers
from account import models


class GlobalDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GlobalDict
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(GlobalDictSerializer, self).to_representation(instance)
        return ret


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(RoleSerializer, self).to_representation(instance)
        return ret


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menus
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # children = instance.get_sub_children()
        children = instance.children
        if children:
            ret['children'] = MenusSerializer(children, many=True).data
        return ret


class MenusTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Menus
        fields = '__all__'

    def get_children(self, instance):
        # children = instance.get_sub_children()
        children = instance.children
        if children:
            serializer = MenusSerializer(children, many=True)
            return serializer.data


class OrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organizations
        fields = '__all__'


class OrganizationTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, instance):
        children = instance.children
        if children:
            serializer = OrganizationsSerializer(children, many=True)
            return serializer.data

    class Meta:
        model = models.Organizations
        fields = '__all__'
