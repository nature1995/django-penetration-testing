# -*- coding: utf-8 -*-
# @Time    : 2/27/20 2:01 PM
# @Author  : naturegong
# @File    : serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserRegSerializer(serializers.ModelSerializer):

    # 验证用户名是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    # 输入密码的时候不显示明文write_only=True
    password = serializers.CharField(style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,)

    # 调用父类的create方法，该方法会返回当前model的实例化对象即user。
    # 前面是将父类原有的create进行执行，后面是加入自己的逻辑
    # 密码加密保存
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict
    def validate(self, attrs):
        # 前端没有传mobile值到后端，这里添加进来
        attrs["mobile"] = attrs["username"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = User
        fields = ("username", "name", "gender", "birthday", "email", "mobile")
