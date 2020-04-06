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

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import UserViewset
from Penetration.settings import MEDIA_ROOT

from users.views import index


router = DefaultRouter()
router.register(r'users', UserViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，传入配置好的MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 自动生成文档
    url(r'docs/', include_docs_urls(title="接口文档")),

    path(r'asset/', include('asset.urls')),
    path(r'info/', include('info.urls')),
    url(r'^$', index, name='index'),

    # path('', include(router.urls)),

    url(r'^login/$', TokenObtainPairView.as_view(), name='login'),
    url(r'^api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
