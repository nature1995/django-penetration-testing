from django.contrib import admin

# Register your models here.
from .models import DomainList

# class DomainListAdmin(admin.ModelAdmin):
#     list_display = ['domain', 'ipaddress']
#     list_filter = ['domain', 'ipaddress']
#     search_fields = ['domain', 'ipaddress']
#     list_display_links = ['domain', 'ipaddress']
#
#
# admin.site.register(DomainList,DomainListAdmin)
