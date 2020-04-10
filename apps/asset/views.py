from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from asset.models import *
from asset.forms import *
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def domain_list(request):
    # 定义域名列表
    domainlist = DomainList.objects.all()
    return render(request, 'asset/asset_domain_list.html', {'DomainList': domainlist})


@login_required(login_url="login")
def domain_manage(request, aid=None, action=None):
    # 定义域名新建和删除页面
    page_name = 'Domain manage'
    if aid:
        domain_list = get_object_or_404(DomainList, pk=aid)

        if action == 'edit':
            page_name = 'Edit domain'
        if action == 'delete':
            domain_list.delete()
            return redirect('Domain list')

    else:
        domain_list = DomainList()
        action = 'add'
        page_name = 'add_domain'

    if request.method == 'POST':
        form = DomainForms(request.POST, instance=domain_list)

        if form.is_valid():
            if action == 'add':
                form.save()
                return redirect('Domain list')
            if action == 'edit':
                form.save()
                return redirect('Domain list')
    else:
        form = DomainForms(instance=domain_list)

    return render(request, 'asset/asset_domain_manage.html',
                  {"form": form, "page_name": page_name, "action": action})
