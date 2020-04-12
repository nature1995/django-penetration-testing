#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : naturegong
# @File    : forms.py
# @Time    : 4/10/20 4:05 PM
from captcha.fields import CaptchaField
from django import forms

from users.models import UserProfile


class LoginForm(forms.Form):
    """登录表单验证"""
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """验证码form & 注册表单form"""
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": "Verification code error"})


class UserInfoForm(forms.ModelForm):
    """用于个人中心修改个人信息"""
    class Meta:
        model = UserProfile
        fields = ['name', 'gender', 'birthday', 'email', 'mobile']
