"""Penetration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.views.static import serve
from Penetration.settings import MEDIA_ROOT
from users.views import index, LoginView, RegisterView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    # user app的url配置
    path("users/", include('users.urls', namespace="users")),

    url(r'^$', index, name="index"),

    path(r'asset/', include('asset.urls')),
    path(r'info/', include('info.urls')),
    path(r'index/', index, name='index'),

    path('login/', LoginView.as_view(), name="login"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    # 注册url
    path(r"register/", RegisterView.as_view(), name="register"),
    # 验证码url
    path(r"captcha/", include('captcha.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，传入配置好的MEDIAROOT
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # path('', include(router.urls)),
    # url(r'^login/$', TokenObtainPairView.as_view(), name='login'),
    # url(r'^api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
