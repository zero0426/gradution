import datetime
import time
from user import models
import pandas as pd
import numpy as np
from django.shortcuts import render, HttpResponse, redirect
from user.system import strategy, transaction_order


def update(request):
    username = request.session.get('info')['username']
    update_account(username)
    update_position(username)
    update_entrust(username)
    update_deal(username)
    update_strategy(username)
    return redirect('/account_info/')


# def update_strategy(request):
#     update_deal(request.session.get('info')['username'])
#     s = request.POST.get('strategy')
#     strategy.update_strategy(request.session.get('info')['username'], s)
#     return redirect('/profit/')


def update_account(username):
    """
    更新资金账户信息
    :param username:
    :return:
    """
    account_path = r"D:\Project\options_strategy_trading_system\output\account.csv"
    account_data = np.asarray(pd.read_csv(account_path, encoding="GBK")[['资金账号', '账号名称', '总资产', '可用金额']])
    for account in account_data:
        account_info = models.FundAccount.objects.filter(username=username, fund_account=account[0]).first()
        if account_info is not None:
            # 账户信息已存在，更新最新信息
            account_info.asset = account[2]
            account_info.avail_funds = account[3]
            account_info.save()
        else:
            # 不存在该信息，插入数据库
            new_info = models.FundAccount(username=username, fund_account=account[0], account_name=account[1],
                                          asset=account[2], avail_funds=account[3])
            new_info.save()


def update_position(username):
    """
    更新持仓信息
    :param username:
    :return:
    """
    position_path = r"D:\Project\options_strategy_trading_system\output\position.csv"
    position_data = np.asarray(pd.read_csv(position_path, encoding="GBK")[
                                   ['资金账号', '账号名称', '证券代码', '证券名称', '当前拥股', '持仓成本', '盈亏',
                                    '盈亏比例', '持仓类型']])
    for position in position_data:
        position_info = models.Position.objects.filter(username=username, fund_account=position[0],
                                                       option_code=position[2], position_type=position[8]).first()
        if position_info is not None:
            # 存在，更新
            position_info.position_volume = position[4]
            position_info.holding_cost = position[5]
            position_info.profit_loss = position[6]
            position_info.profit_loss_ratio = position[7]
            position_info.save()
        else:
            # 不存在，插入
            new_info = models.Position(username=username, fund_account=position[0], option_code=position[2],
                                       option_name=position[3], position_volume=position[4], holding_cost=position[5],
                                       profit_loss=position[6], profit_loss_ratio=position[7],
                                       position_type=position[8])
            new_info.save()


def update_entrust(username):
    """
    更新委托信息
    :param username:
    :return:
    """
    entrust_path = r"D:\Project\options_strategy_trading_system\output\entrust.csv"
    entrust_data = np.asarray(pd.read_csv(entrust_path, encoding="GBK")[
                                  ['资金账号', '下单方式', '证券代码', '证券名称', '操作', '开平', '委托价格',
                                   '委托量', '委托状态',
                                   '成交数量', '成交均价', '委托来源', '任务编号']])
    for entrust in entrust_data:
        if entrust[11] == "本终端" and entrust[8] != "废单":
            entrust_info = models.Entrust.objects.filter(entrust_id=entrust[12], username=username,
                                                         fund_account=entrust[0]).first()
            if entrust_info is None:
                # 不存在，插入
                now_info = models.Entrust(entrust_id=entrust[12], username=username, fund_account=entrust[0],
                                          way=entrust[1], option_code=entrust[2], option_name=entrust[3],
                                          buy_sell=entrust[4], open_close=entrust[5], entrust_price=entrust[6],
                                          entrust_quantity=entrust[7], statue=entrust[8], quantity=entrust[9],
                                          price=entrust[10])
                now_info.save()
            else:
                entrust_info.way = entrust[1]
                entrust_info.option_code = entrust[2]
                entrust_info.option_name = entrust[3]
                entrust_info.buy_sell = entrust[4]
                entrust_info.open_close = entrust[5]
                entrust_info.entrust_price = entrust[6]
                entrust_info.entrust_quantity = entrust[7]
                entrust_info.statue = entrust[8]
                entrust_info.quantity = entrust[9]
                entrust_info.price = entrust[10]
                entrust_info.save()


def update_deal(username):
    """
    更新成交信息
    :param username:
    :return:
    """
    flag = False
    deal_path = r"D:\Project\options_strategy_trading_system\output\deal.csv"
    deal_data = np.asarray(pd.read_csv(deal_path, encoding="GBK")[
                               ['资金账号', '账号名称', '证券代码', '证券名称', '成交编号', '买卖', '开平', '成交价格',
                                '成交数量', '成交日期', '成交时间', '手续费', '委托来源']])
    for deal in deal_data:
        if deal[12] == "本终端":
            deal_info = models.Transaction.objects.filter(deal_id=deal[4], username=username,
                                                          fund_account=deal[0]).first()
            if deal_info is None:
                # 不存在，插入
                new_info = models.Transaction(deal_id=deal[4], username=username, fund_account=deal[0],
                                              option_code=deal[2],
                                              option_name=deal[3], buy_sell=deal[5], open_close=deal[6], price=deal[7],
                                              quantity=deal[8], premium=deal[11])
                new_info.save()
                flag = True
    return flag


def update_strategy(username):
    """
    更新已采用的策略
    :param username:
    :return:
    """
    single_strategy_info = models.SingleStrategy.objects.filter(username=username)
    composite_strategy_info = models.CompositeStrategy.objects.filter(username=username)
    # 更新单腿策略
    for info in single_strategy_info:
        if info.quantity == 0:
            data = models.Transaction.objects.filter(username=username, option_code=info.option_code, date=info.date,
                                                     open_close="开仓").last()
            entrust_data = models.Entrust.objects.filter(username=username, option_code=info.option_code,
                                                         date=info.date,
                                                         open_close="开仓", statue="已成").last()
            if data is not None:
                info.option_name = data.option_name
                info.buy_sell = data.buy_sell
                info.price = data.price
                info.quantity = data.quantity
            elif entrust_data is not None:
                info.option_name = entrust_data.option_name
                info.buy_sell = entrust_data.buy_sell
                info.price = entrust_data.price
                info.quantity = entrust_data.quantity
            info.save()
    # 更新复合策略
    for composite_info in composite_strategy_info:
        if composite_info.quantity_buy == 0 or composite_info.quantity_sell == 0:
            data_buy = models.Transaction.objects.filter(username=username, option_code=composite_info.option_code_buy,
                                                         date=composite_info.date, open_close="开仓").last()
            data_sell = models.Transaction.objects.filter(username=username,
                                                          option_code=composite_info.option_code_sell,
                                                          date=composite_info.date, open_close="开仓").last()
            entrust_data_buy = models.Entrust.objects.filter(username=username,
                                                             option_code=composite_info.option_code_buy,
                                                             date=composite_info.date,
                                                             open_close="开仓", statue="已成").last()
            entrust_data_sell = models.Entrust.objects.filter(username=username,
                                                              option_code=composite_info.option_code_sell,
                                                              date=composite_info.date,
                                                              open_close="开仓", statue="已成").last()
            if data_buy is not None:
                # 有成交记录
                composite_info.option_name_buy = data_buy.option_name
                composite_info.price_buy = data_buy.price
                composite_info.quantity_buy = data_buy.quantity
            elif entrust_data_buy is not None:
                # 没有成交记录，到已完成的委托中查询数据
                composite_info.option_name_buy = entrust_data_buy.option_name
                composite_info.price_buy = entrust_data_buy.price
                composite_info.quantity_buy = entrust_data_buy.quantity
            if data_sell is not None:
                composite_info.option_name_sell = data_sell.option_name
                composite_info.price_sell = data_sell.price
                composite_info.quantity_sell = data_sell.quantity
            elif entrust_data_sell is not None:
                composite_info.option_name_sell = entrust_data_sell.option_name
                composite_info.price_sell = entrust_data_sell.price
                composite_info.quantity_sell = entrust_data_sell.quantity
            composite_info.save()


def add_strategy(username, strategy_name, date, strategy_info):
    """
    添加策略
    :param username:
    :param strategy_name: 策略名称
    :param date: 日期
    :param strategy_info:
    :return:
    """
    if strategy_name == "后市大涨" or strategy_name == "后市不跌":
        info = models.Transaction.objects.filter(username=username, option_code=strategy_info[0], date=date,
                                                 open_close="开仓").last()
        if info is not None:
            add_info = models.SingleStrategy(username=username, strategy_name=strategy_name,
                                             option_code=info.option_code, option_name=info.option_name,
                                             buy_sell=info.buy_sell, price=info.price, quantity=info.quantity)
        else:
            add_info = models.SingleStrategy(username=username, strategy_name=strategy_name,
                                             option_code=strategy_info[0])
        add_info.save()
    elif strategy_name == "温涨" or strategy_name == "温涨坐庄":
        info_buy = models.Transaction.objects.filter(username=username, option_code=strategy_info[0][0],
                                                     date=date, open_close="开仓").last()
        info_sell = models.Transaction.objects.filter(username=username, option_code=strategy_info[1][0],
                                                      date=date, open_close="开仓").last()
        if info_buy is not None and info_sell is not None:
            add_info = models.CompositeStrategy(username=username, strategy_name=strategy_name,
                                                option_code_buy=info_buy.option_code,
                                                option_name_buy=info_buy.option_name, price_buy=info_buy.price,
                                                quantity_buy=info_buy.quantity, option_code_sell=info_sell.option_code,
                                                option_name_sell=info_sell.option_name, price_sell=info_sell.price,
                                                quantity_sell=info_sell.quantity)
        elif info_buy is None:
            add_info = models.CompositeStrategy(username=username, strategy_name=strategy_name,
                                                option_code_buy=strategy_info[0][0],
                                                option_code_sell=info_sell.option_code,
                                                option_name_sell=info_sell.option_name, price_sell=info_sell.price,
                                                quantity_sell=info_sell.quantity)
        elif info_sell is None:
            add_info = models.CompositeStrategy(username=username, strategy_name=strategy_name,
                                                option_code_buy=info_buy.option_code,
                                                option_name_buy=info_buy.option_name, price_buy=info_buy.price,
                                                quantity_buy=info_buy.quantity,
                                                option_code_sell=strategy_info[1][0])
        else:
            add_info = models.CompositeStrategy(username=username, strategy_name=strategy_name,
                                                option_code_buy=strategy_info[0][0],
                                                option_code_sell=strategy_info[1][0])
        add_info.save()


def delete_strategy(username, strategy_name, date, ti):
    if strategy_name == "后市大涨" or strategy_name == "后市不跌":
        info = models.SingleStrategy.objects.filter(username=username, strategy_name=strategy_name, date=date,
                                                    time=ti).first()
        if info.quantity != 0:
            # 平仓
            if info.buy_sell == "买入":
                transaction_order.generate_transaction_order('49', '1', info.option_code, info.quantity)
            else:
                transaction_order.generate_transaction_order('51', '1', info.option_code, info.quantity)
        info.delete()
    elif strategy_name == "温涨" or strategy_name == "温涨坐庄":
        info = models.CompositeStrategy.objects.filter(username=username, strategy_name=strategy_name, date=date,
                                                       time=ti).first()
        if info.quantity_buy != 0:
            # 卖出平仓
            transaction_order.generate_transaction_order('49', '1', info.option_code_buy, info.quantity_buy)
        if info.quantity_buy != 0:
            # 买入平仓
            transaction_order.generate_transaction_order('51', '1', info.option_code_sell, info.quantity_sell)
        info.delete()
