import random
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# Django自带的用户验证,login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
# 并集运算
from django.db.models import Q
# 基于类实现需要继承的view
from django.views.generic.base import View

from .forms import LoginForm, RegisterForm, UserInfoForm
from .models import UserProfile
# 进行密码加密
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.


class CustomBackend(ModelBackend):
    """
    Custom user authentication rules
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = UserProfile.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        # django自带的logout
        logout(request)
        # 重定向到首页,
        return HttpResponseRedirect(reverse("login"))


class LoginView(View):
    # 直接调用get方法免去判断
    def __init__(self):
        super(LoginView, self).__init__()
        self.page_name = 'Login'

    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        redirect_url = request.GET.get('next', '')
        return render(request, "login.html", {"redirect_url": redirect_url, "page_name": self.page_name})

    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的usernamepassword，会对应到form中
        login_form = LoginForm(request.POST)

        # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null说明验证成功
            if user is not None:
                # 只有当用户激活时才给登录
                if user.is_active:
                    # login_in 两参数：request, user
                    # 实际是对request写了一部分东西进去，然后在render的时候：
                    # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    # 增加重定向回原网页。
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    # 跳转到首页 user request会被带回到首页
                    return HttpResponseRedirect(reverse("index"))
                # 即用户未激活跳转登录，提示未激活
                else:
                    return render(
                        request, "login.html", {"msg": "Username is not activated! Please go to the mailbox to activate", "page_name": self.page_name})
            # 仅当用户真的密码出错时
            else:
                return render(request, "login.html", {"msg": "Wrong user name or password!"})
        # 验证不成功跳回登录页面
        # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(
                request, "login.html", {"login_form": login_form, "page_name": self.page_name})


class RegisterView(View):
    """注册功能的view"""
    def __init__(self):
        super(RegisterView, self).__init__()
        self.page_name = 'Registration'

    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form, "page_name": self.page_name})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时前端的name为email
            user_name = request.POST.get("email", "")
            # 用户查重
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "User already exists"})
            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为True
            user_profile.is_active = True

            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 跳转到登录页面
            return render(request, "login.html")
        # 注册邮箱form验证失败
        else:
            return render(
                request, "register.html", {"register_form": register_form})


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def __init__(self):
        super(UserInfoView, self).__init__()
        self.page_name = 'Profile'

    def get(self, request):
        return render(request, "user_info.html", {"page_name": self.page_name})

    def post(self, request):
        # 不像用户咨询是一个新的。需要指明instance。不然无法修改，而是新增用户
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


@login_required(login_url="login")
def index(request):
    user_num = len(UserProfile.objects.all())
    data = {
        'page_name': 'Dash board',
        'user_num': user_num,
    }
    return render(request, 'index.html', data)
