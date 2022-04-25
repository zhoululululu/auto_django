# -*- coding: utf-8 -*- 
"""
Created on 2021/11/17 22:00 
@File  : manage_user.py
@author: zhoul
@Desc  :
"""

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse


def login(request):
    if request.method == "GET":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # 验证成功，返回user对象，否则返回None
        user = auth.authenticate(username=user, password=pwd)

    return HttpResponse("Hello world ! ")


def create_user(request):
    if request.method == "POST":
        user = request.POST.get("user")
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        print(user, email, pwd)
        user = User.objects.create_user(user, email, pwd)
        user.save()
    return HttpResponse("create user success! ")
