from django.db import models


# Create your models here.


# 用户信息
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=16)


# 资金账户
class FundAccount(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16)
    fund_account = models.CharField(verbose_name="资金账户", max_length=16)
    account_name = models.CharField(verbose_name="账号名称", max_length=16)
    asset = models.DecimalField(verbose_name="总资产", max_digits=14, decimal_places=2, default=0)
    avail_funds = models.DecimalField(verbose_name="可用资金", max_digits=14, decimal_places=2, default=0)


# 持仓情况
class Position(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16)
    fund_account = models.CharField(verbose_name="资金账户", max_length=16)
    option_code = models.CharField(verbose_name="合约代码", max_length=8)
    option_name = models.CharField(verbose_name="合约简称", max_length=20)
    position_volume = models.IntegerField(verbose_name="持仓量")
    holding_cost = models.DecimalField(verbose_name="持仓成本", max_digits=10, decimal_places=4)
    profit_loss = models.DecimalField(verbose_name="盈亏", max_digits=10, decimal_places=2)
    profit_loss_ratio = models.CharField(verbose_name="盈亏比例", max_length=10)
    position_type = models.CharField(verbose_name="持仓类型", max_length=6)


# 委托
class Entrust(models.Model):
    entrust_id = models.CharField(verbose_name="委托编号", max_length=16, default="")
    username = models.CharField(verbose_name="用户名", max_length=16, default="")
    fund_account = models.CharField(verbose_name="资金账户", max_length=16, default="")
    way = models.CharField(verbose_name="下单方式", max_length=16, default="")
    option_code = models.CharField(verbose_name="合约代码", max_length=8, default="")
    option_name = models.CharField(verbose_name="合约简称", max_length=20, default="")
    buy_sell = models.CharField(verbose_name="买卖方向", max_length=8, default="")
    open_close = models.CharField(verbose_name="开平仓", max_length=8, default="")
    entrust_price = models.DecimalField(verbose_name="委托价格", max_digits=10, decimal_places=4, default=0)
    entrust_quantity = models.IntegerField(verbose_name="委托数量", default=0)
    statue = models.CharField(verbose_name="委托状态", max_length=16, default="")
    quantity = models.IntegerField(verbose_name="成交数量", default=0)
    price = models.DecimalField(verbose_name="成交均价", max_digits=10, decimal_places=4, default=0)
    date = models.DateField(verbose_name="创建日期", auto_now_add=True)
    time = models.TimeField(verbose_name="创建时间", auto_now_add=True)


# 交易记录
class Transaction(models.Model):
    deal_id = models.CharField(verbose_name="交易编号", max_length=16, default="")
    username = models.CharField(verbose_name="用户名", max_length=16, default="")
    fund_account = models.CharField(verbose_name="资金账户", max_length=16, default="")
    option_code = models.CharField(verbose_name="合约代码", max_length=8, default="")
    option_name = models.CharField(verbose_name="合约简称", max_length=20, default="")
    buy_sell = models.CharField(verbose_name="买卖方向", max_length=8, default="")
    open_close = models.CharField(verbose_name="开平仓", max_length=8, default="")
    price = models.DecimalField(verbose_name="交易价格", max_digits=10, decimal_places=4, default=0)
    quantity = models.IntegerField(verbose_name="数量", default=0)
    premium = models.DecimalField(verbose_name="手续费", max_digits=8, decimal_places=2, default=0)
    date = models.DateField(verbose_name="创建日期", auto_now_add=True)
    time = models.TimeField(verbose_name="创建时间", auto_now_add=True)


# 单腿策略
class SingleStrategy(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16, default="")
    strategy_name = models.CharField(verbose_name="策略名称", max_length=16)
    option_code = models.CharField(verbose_name="合约代码", max_length=8, default="")
    option_name = models.CharField(verbose_name="合约简称", max_length=20, default="")
    buy_sell = models.CharField(verbose_name="买卖方向", max_length=8, default="")
    price = models.DecimalField(verbose_name="交易价格", max_digits=10, decimal_places=4, default=0)
    quantity = models.IntegerField(verbose_name="数量", default=0)
    date = models.DateField(verbose_name="创建日期", auto_now_add=True)
    time = models.TimeField(verbose_name="创建时间", auto_now_add=True)


# 复合策略
class CompositeStrategy(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16, default="")
    strategy_name = models.CharField(verbose_name="策略名称", max_length=16)
    option_code_buy = models.CharField(verbose_name="合约代码", max_length=8, default="")
    option_name_buy = models.CharField(verbose_name="合约简称", max_length=20, default="")
    price_buy = models.DecimalField(verbose_name="交易价格", max_digits=10, decimal_places=4, default=0)
    quantity_buy = models.IntegerField(verbose_name="数量", default=0)
    option_code_sell = models.CharField(verbose_name="合约代码", max_length=8, default="")
    option_name_sell = models.CharField(verbose_name="合约简称", max_length=20, default="")
    price_sell = models.DecimalField(verbose_name="交易价格", max_digits=10, decimal_places=4, default=0)
    quantity_sell = models.IntegerField(verbose_name="数量", default=0)
    date = models.DateField(verbose_name="创建日期", auto_now_add=True)
    time = models.TimeField(verbose_name="创建时间", auto_now_add=True)


# 期权日频率数据
class option_daily_info(models.Model):
    option_code = models.CharField(verbose_name="合约代码", max_length=8)
    option_name = models.CharField(verbose_name="期权合约简称", max_length=30)
    date = models.DateField(verbose_name="日期")
    open_price = models.DecimalField(verbose_name="开盘价", max_digits=10, decimal_places=4)
    close_price = models.DecimalField(verbose_name="收盘价", max_digits=10, decimal_places=4)
    highest_price = models.DecimalField(verbose_name="最高价", max_digits=10, decimal_places=4)
    lowest_price = models.DecimalField(verbose_name="最低价", max_digits=10, decimal_places=4)
    transaction_num = models.IntegerField(verbose_name="成交量")
    turnover = models.DecimalField(verbose_name="成交额", max_digits=14, decimal_places=4)
