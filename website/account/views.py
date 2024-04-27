from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from account import models
from account import serializers
from components.pagination import SizeTablePageNumberPagination


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menus.objects.all()
    serializer_class = serializers.MenusSerializer
    pagination_class = SizeTablePageNumberPagination
