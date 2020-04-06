from django.db import models

# Create your models here.


class DomainList(models.Model):
    # id = models.CharField('序号', max_length=50, primary_key=True)
    domain = models.CharField(u'Domain', max_length=50,unique=False,null=True)
    ipaddress = models.GenericIPAddressField(u'IP', protocol='both',null=True,unique=False)
    subdomain = models.CharField(u'Sub Domain', max_length=50, null=True, unique=True)

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name_plural = u'域名管理'

