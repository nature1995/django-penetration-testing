# Generated by Django 2.1.5 on 2019-02-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0004_auto_20190209_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainlist',
            name='subdomain',
            field=models.CharField(max_length=50, null=True, verbose_name='Sub Domain'),
        ),
        migrations.AlterField(
            model_name='domainlist',
            name='domain',
            field=models.CharField(max_length=50, unique=True, verbose_name='Sub Domain'),
        ),
    ]
