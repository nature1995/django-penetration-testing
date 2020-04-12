#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : naturegong
# @File    : urls.py
# @Time    : 4/11/20 7:18 PM
from users.views import UserInfoView
from django.urls import path
app_name = "users"

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name="user_info"),
]
