# Generated by Django 4.1.7 on 2023-02-26 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='pwd',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='name',
            new_name='username',
        ),
    ]