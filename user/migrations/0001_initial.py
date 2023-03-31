# Generated by Django 4.1.7 on 2023-02-26 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=16, verbose_name='密码')),
                ('is_bind', models.BooleanField(verbose_name='是否绑定证券账户')),
                ('asset', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='总资产')),
            ],
        ),
    ]