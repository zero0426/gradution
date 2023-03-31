import akshare as ak
import numpy as np
from decimal import Decimal

# from user import models


"""
策略分析
"""
"""
0.买量 1.买价 2.最新价 3.卖价 4.卖量 5.持仓量 6.涨幅 7.行权价 8.昨收价 9.开盘价 10.涨停价 11.跌停价
12.申卖价五 13.申卖量五 14.申卖价四 15.申卖量四 16.申卖价三 17.申卖量三 18.申卖价二 19.申卖量二 20.申卖价一 21.申卖量一
22.申买价一 23.申买量一 24.申买价二 25.申买量二 26.申买价三 27.申买量三 28.申买价四 29.申买量四 30.申买价五 31.申买量五
32.行情时间 33.主力合约标识 34.状态码 35.标的证券类型 36.标的股票 37.期权合约简称 38.振幅 39.最高价 40.最低价 41.成交量 42.成交额
"""


def get_bond(id):
    return


def get_all_info():
    call_info = np.empty([0, 14], str)
    put_info = np.empty([0, 14], str)
    months = ak.option_sse_list_sina()
    for month in months:
        call_code = np.asarray(ak.option_sse_codes_sina("看涨期权", month, '510050'))[:, 1]
        put_code = np.asarray(ak.option_sse_codes_sina("看跌期权", month, '510050'))[:, 1]
        for code in call_code:
            spot_price = np.asarray(ak.option_sse_spot_price_sina(code))[:, 1]
            greeks = np.asarray(ak.option_sse_greeks_sina(code))[:, 1]
            # 期权简称，代码，到期月份，行权价，卖价，买价，涨幅，最新价，成交量，Delta，Gamma，Theta，Vega，隐含波动率
            a = np.asarray([spot_price[37], code, month, spot_price[7], spot_price[3],
                            spot_price[1], spot_price[6], spot_price[2], spot_price[41],
                            greeks[2], greeks[3], greeks[4], greeks[5], greeks[6]]).reshape((1, 14))
            call_info = np.append(call_info, a, axis=0)
        for code in put_code:
            spot_price = np.asarray(ak.option_sse_spot_price_sina(code))[:, 1]
            greeks = np.asarray(ak.option_sse_greeks_sina(code))[:, 1]
            a = np.asarray([spot_price[37], code, month, spot_price[7], spot_price[3],
                            spot_price[1], spot_price[6], spot_price[2], spot_price[41],
                            greeks[2], greeks[3], greeks[4], greeks[5], greeks[6]]).reshape((1, 14))
            put_info = np.append(put_info, a, axis=0)
    return call_info, put_info


def rising_in_the_future(call_info):
    """
    后市大涨：预期价格上涨。价格上升最大盈利为无限，价格下跌最大损失为权利金花费。
    期权代码，期权简称，Delta,Gamma,Theta,Vega,隐含波动率,权利金,保证金,盈亏平衡点，最大收益，最大损失
    :return:
    """
    months = ak.option_sse_list_sina()
    for info in call_info:
        if info[2] == months[1]:
            if float(info[9]) < 0.45:
                royalty = Decimal(0 - float(info[4]) * 10000).quantize(Decimal("0.00"))
                bond = 0.00
                breakeven = Decimal(float(info[3][0:6]) + float(info[4])).quantize(Decimal("0.0000"))
                max_profit = "无限"
                max_loss = Decimal( 0 - float(info[4]) * 10000).quantize(Decimal("0.00"))
                result = np.asarray([info[1], info[0], info[9], info[10], info[11], info[12], info[13],
                                     royalty, bond, breakeven, max_profit, max_loss])
                return result


def not_falling_in_the_future(put_info):
    """
    后市不跌：预期价格不跌。价格上升最大盈利为权利金收入，价格下降最大损失为全部行权价减去权利金收入。
    :return:
    """
    months = ak.option_sse_list_sina()
    # print(put_info[:,9:])
    for info in put_info:
        if info[2] == months[1]:
            if float(info[9]) < -0.6:
                royalty = Decimal(float(info[5]) * 10000).quantize(Decimal("0.00"))
                bond = 0.00  # get_bond(info[1])
                breakeven = Decimal(float(info[3][0:6]) - float(info[5])).quantize(Decimal("0.0000"))
                max_profit = Decimal(float(info[5]) * 10000).quantize(Decimal("0.00"))
                max_loss = Decimal(0 - (float(info[3][0:6]) - float(info[5])) * 10000).quantize(Decimal("0.00"))
                result = np.asarray([info[1], info[0], info[9], info[10], info[11], info[12], info[13],
                                     royalty, bond, breakeven, max_profit, max_loss])
                return result


def temperature_rise(call_info):
    """
    温涨：预期价格上涨。买进看涨期权，但价格上方有压力位，卖出较高执行价的看涨期权增加收入。此策略限制了价格大涨时的收益，但增加了价格小涨时的收益。盈亏均有限。
    :return:
    """
    price = np.asarray(ak.fund_open_fund_info_em('510050')[-1:])[:, 1]
    months = ak.option_sse_list_sina()
    buy = []
    sell = []
    for info in call_info:
        if info[2] == months[1]:
            if 0.5 < float(info[9]) < 0.7:
                if len(buy) == 0:
                    buy = [info[1], info[0], info[9], info[10], info[11], info[12], info[13],
                           Decimal(0 - float(info[4])).quantize(Decimal("0.00")) * 10000, 0.0, info[3][0:6]]
            if 0.5 > float(info[9]) > 0.3:
                if len(sell) == 0:
                    sell = [info[1], info[0], info[9], info[10], info[11], info[12], info[13], Decimal(float(info[5]) * 10000).quantize(Decimal("0.00")),
                            0.0, info[3][0:6]]

    # 盈亏平衡点： 较低行权价+建仓成本
    breakeven = Decimal(float(buy[-1]) - (float(buy[7]) + float(sell[7])) / 10000).quantize(Decimal("0.0000"))
    # 最大收益 : 较高行权价-较低行权价-买入认购期权权利金+卖出认购期权权利金
    max_profit =Decimal((float(sell[-1]) - float(buy[-1])) * 10000 + float(buy[7]) + float(sell[7])).quantize(Decimal("0.00"))
    # 最大损失：卖出认购期权权利金-买入认购期权权利金
    max_loss = Decimal(float(buy[7]) + float(sell[7])).quantize(Decimal("0.00"))
    result = [buy, sell, breakeven, max_profit, max_loss]
    return result


def temperature_rise_sit(put_info):
    """
    温涨坐庄：预期价格不跌。卖出看跌期权，赚取权力金。为防止价格大跌，买进较低执行价的看跌期权限制损失。盈亏均有限。
    :return:
    """
    months = ak.option_sse_list_sina()
    buy = []
    sell = []
    for info in put_info:
        if info[2] == months[1]:
            if -0.5 < float(info[9]) < -0.3:
                if len(buy) == 0:
                    buy = [info[1], info[0], info[9], info[10], info[11], info[12], info[13],
                           Decimal(0 - float(info[4]) * 10000).quantize(Decimal("0.00")), 0.0, info[3][0:6]]
            if -0.7 < float(info[9]) < -0.5:
                if len(sell) == 0:
                    sell = [info[1], info[0], info[9], info[10], info[11], info[12], info[13], Decimal(float(info[5]) * 10000).quantize(Decimal("0.00")),
                            0.0, info[3][0:6]]

    # 盈亏平衡点： 较低行权价+建仓成本
    breakeven = Decimal(float(sell[-1]) + (float(buy[7]) + float(sell[7])) / 10000).quantize(Decimal("0.0000"))
    # 最大收益 : 卖出认购期权权利金+买入认购期权权利金
    max_profit = Decimal(float(buy[7]) + float(sell[7])).quantize(Decimal("0.00"))
    # 最大损失：较高行权价-较低行权价-买入认购期权权利金+卖出认购期权权利金
    max_loss = Decimal(0 - (float(sell[-1]) - float(buy[-1])) * 10000 + float(buy[7]) + float(sell[7])).quantize(
                Decimal("0.00"))
    result = [buy, sell, breakeven, max_profit, max_loss]
    return result


def bull_positive_buy(buy_info, sell_info):
    """
    牛市正购：预期后市盘整或者上涨的概率很大，在近月较高行权价合约开义务仓赚取时间价值，在远月较低行权价合约开权力仓赚取价格波动的收益。
    :return:
    """




    pass


def bull_positive_sell():
    """
    牛市正沽：预期近期盘整或上涨的概率很大，卖出近月较高行权价认沽期权赚取时间价值，同时花费少量的权利金买入远月低行权价的认沽期权以防后市看跌。
    :return:
    """
    pass


def bull_negative_buy():
    """
    牛市反购：预期近期上涨的概率很大，未来涨幅趋平，买入近月较低行权价合约看涨后市，
            卖出远月较高行权价合约收益一部分权利金，同时可能赚回波动率下降的额外收益。
    :return:
    """
    pass


def bull_negative_sell():
    """
    牛市反沽：预期后市上涨的可能性较大，卖出远月高行权价的认沽期权同时买入近月的低行权价的认沽期权，
            如果未来后市小幅上涨的话，可以在损失小部分权力金的代价的基础上赚取较大的权利金。
    :return:
    """
    pass


def buy_call(month):
    """
    买入认购
    :return:
    """
    analysis = np.empty([0, 13], str)
    call_code = np.asarray(ak.option_sse_codes_sina("看涨期权", month, '510050'))[:, 1]
    for code in call_code:
        contract_info = np.asarray(ak.option_sse_spot_price_sina(code))[:, 1]
        # 盈亏平衡点：行权价+卖价
        breakeven = Decimal(float(contract_info[7]) + float(contract_info[3])).quantize(Decimal("0.0000"))
        # 最大收益
        max_profit = '∞'
        # 最大损失：全部权利金
        max_loss = 0 - Decimal(float(contract_info[3]) * 10000).quantize(Decimal("0.00"))
        # 开仓保证金：
        bond = 0.00
        # 开仓权利金
        royalty = Decimal(float(contract_info[3]) * 10000).quantize(Decimal("0.00"))
        # 合约代码，期权合约简称，持仓量，卖量，卖价，买量，买价，涨幅，最新价，盈亏平衡点，最大收益,最大损失，开仓保证金，开仓权利金
        a = np.asarray([code, contract_info[37], contract_info[5], contract_info[4],
                        contract_info[3], contract_info[0], contract_info[1], contract_info[6],
                        breakeven, max_profit, max_loss, bond, royalty]).reshape((1, 13))

        analysis = np.append(analysis, a, axis=0)
    return analysis


def sell_put(month):
    """
    卖出认沽
    :return:
    """
    analysis = np.empty([0, 14], str)
    put_code = np.asarray(ak.option_sse_codes_sina("看跌期权", month, '510050'))[:, 1]
    for code in put_code:
        contract_info = np.asarray(ak.option_sse_spot_price_sina(code))[:, 1]
        # 盈亏平衡点，行权价-买价
        breakeven = Decimal(float(contract_info[7]) - float(contract_info[1])).quantize(Decimal("0.0000"))
        # 最大收益：权利金
        max_profit = Decimal(float(contract_info[3]) * 10000).quantize(Decimal("0.00"))
        # 最大损失：行权价*10000-开仓权利金
        max_loss = 0 - Decimal((float(contract_info[7]) - float(contract_info[3])) * 10000).quantize(Decimal("0.00"))
        # 开仓保证金：
        bond = 0.00
        # 开仓权利金
        royalty = float(contract_info[3]) * 10000


def bull_call_price_difference(month):
    """
    牛市认购价差,买入较低行权价的认购期权，卖出较高行权价的认购期权
    :return:
    """
    call_code = np.asarray(ak.option_sse_codes_sina("看涨期权", month, '510050'))[:, 1]
    analysis = np.empty([0, 7], dtype=object)
    info = np.empty([0, 8])
    for code in call_code:
        contract_info = np.asarray(ak.option_sse_spot_price_sina(code))[:, 1]
        # 合约代码，行权价，持仓量，卖量，卖价，买量，买价，涨幅
        a = np.asarray([code, float(contract_info[7][0:6]), contract_info[5], contract_info[4], contract_info[3],
                        contract_info[0], contract_info[1], contract_info[6]]).reshape(1, 8)
        info = np.append(info, a, axis=0)
    info = info[np.argsort(info[:, 1])]
    for i in range(info.shape[0] - 1):
        for j in range(i + 1, info.shape[0]):
            # 盈亏平衡点：较低行权价+建仓成本
            breakeven = float(
                Decimal(float(info[i, 1]) - float(info[j, 6]) + float(info[i, 4])).quantize(Decimal("0.0000")))
            # 最大收益 : 较高行权价-较低行权价-买入认购期权权利金+卖出认购期权权利金
            max_profit = float(Decimal(
                (float(info[j, 1]) - float(info[i, 1]) - float(info[i, 4]) + float(info[j, 6])) * 10000).quantize(
                Decimal("0.00")))
            # 最大损失：卖出认购期权权利金-买入认购期权权利金
            max_loss = float(Decimal((float(info[j, 6]) - float(info[i, 4])) * 10000).quantize(Decimal("0.00")))
            # 开仓保证金：
            bond = 0.00
            # 开仓权利金
            royalty = float(Decimal((float(info[j, 6]) - float(info[i, 4])) * 10000).quantize(Decimal("0.00")))
            # 买入期权信息,卖出期权信息
            a = np.asarray([info[i], info[j], breakeven, max_profit, max_loss, bond, royalty], dtype=object).reshape(1,
                                                                                                                     7)
            if max_profit > 0:
                analysis = np.append(analysis, a, axis=0)
    return analysis


def bull_put_price_difference():
    pass
