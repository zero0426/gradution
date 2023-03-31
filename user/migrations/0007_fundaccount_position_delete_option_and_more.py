# Generated by Django 4.1.7 on 2023-03-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_option_daily_info_close_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, verbose_name='用户名')),
                ('fund_account', models.CharField(max_length=16, verbose_name='资金账户')),
                ('account_name', models.CharField(max_length=16, verbose_name='账号名称')),
                ('asset', models.DecimalField(decimal_places=2, default=0, max_digits=14, verbose_name='总资产')),
                ('avail_funds', models.DecimalField(decimal_places=2, default=0, max_digits=14, verbose_name='可用资金')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, verbose_name='用户名')),
                ('fund_account', models.CharField(max_length=16, verbose_name='资金账户')),
                ('option_code', models.CharField(max_length=8, verbose_name='合约代码')),
                ('option_name', models.CharField(max_length=20, verbose_name='合约简称')),
                ('position_volume', models.IntegerField(verbose_name='持仓量')),
                ('holding_cost', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='持仓成本')),
                ('profit_loss', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='盈亏')),
                ('profit_loss_ratio', models.CharField(max_length=10, verbose_name='盈亏比例')),
                ('position_type', models.CharField(max_length=6, verbose_name='持仓类型')),
            ],
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='bid_price',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='now_price',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='avail_funds',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='investment',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='is_bind',
        ),
        migrations.AddField(
            model_name='transaction',
            name='deal_id',
            field=models.CharField(default='', max_length=16, verbose_name='交易编号'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='fund_account',
            field=models.CharField(default='', max_length=16, verbose_name='资金账户'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='open_close',
            field=models.CharField(default='', max_length=8, verbose_name='开平仓'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='option_name',
            field=models.CharField(default='', max_length=20, verbose_name='合约简称'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='premium',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='手续费'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10, verbose_name='交易价格'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buy_sell',
            field=models.CharField(default='', max_length=8, verbose_name='买卖方向'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='option_code',
            field=models.CharField(default='', max_length=8, verbose_name='合约代码'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='username',
            field=models.CharField(default='', max_length=16, verbose_name='用户名'),
        ),
    ]
