import random

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets, permissions, authentication, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers import UserRegSerializer, UserDetailSerializer

User = get_user_model()
# Create your views here.


class CustomBackend(ModelBackend):
    """
    Custom user authentication rules
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    User
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication, authentication.SessionAuthentication)
    # permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data

        # 生成注册用户的Token
        re_dict["token"] = str(AccessToken.for_user(user))
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 这里需要动态选择用哪个序列化方式
    # 1.UserRegSerializer（用户注册），只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
    # 2.问题又来了，如果注册的使用UserDetailSerializer，又会导致验证失败，所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # 这里需要动态权限配置
    # 1.用户注册的时候不应该有权限限制
    # 2.当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    # 虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
    # 重写get_object方法，就知道是哪个用户了
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


def index(request):
    data = {
        'page_name': 'Dash board'
    }
    return render(request, 'index.html', data)