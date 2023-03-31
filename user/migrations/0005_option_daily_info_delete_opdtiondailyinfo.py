# Generated by Django 4.1.7 on 2023-03-08 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_opdtiondailyinfo_option_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='option_daily_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_code', models.CharField(max_length=8, verbose_name='合约代码')),
                ('option_name', models.CharField(max_length=30, verbose_name='期权合约简称')),
                ('date', models.DateField(verbose_name='日期')),
                ('open_price', models.DecimalField(decimal_places=4, max_digits=8, verbose_name='开盘价')),
                ('close_price', models.DecimalField(decimal_places=4, max_digits=8, verbose_name='收盘价')),
                ('highest_price', models.DecimalField(decimal_places=4, max_digits=8, verbose_name='最高价')),
                ('lowest_price', models.DecimalField(decimal_places=4, max_digits=8, verbose_name='最低价')),
                ('transaction_num', models.IntegerField(verbose_name='成交量')),
                ('turnover', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='成交额')),
            ],
        ),
        migrations.DeleteModel(
            name='OpdtionDailyInfo',
        ),
    ]