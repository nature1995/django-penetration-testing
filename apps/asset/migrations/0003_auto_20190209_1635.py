# Generated by Django 2.1.5 on 2019-02-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20190209_1253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domainlist',
            options={'verbose_name_plural': '域名管理'},
        ),
        migrations.AlterField(
            model_name='domainlist',
            name='ipaddress',
            field=models.GenericIPAddressField(verbose_name='IP'),
        ),
    ]