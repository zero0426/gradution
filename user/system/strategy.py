import time

from django.shortcuts import render, HttpResponse, redirect
from user.system import strategy_analyse
import akshare as ak
import numpy as np
from user.system import transaction_order as to
from user.system import upload_info as up

global result


def show(request):
    """
    展示生成的策略
    :param request:
    :return:
    """
    global result
    if request.method == "GET":
        """显示全部策略"""
        result = run()
        t_name = ["合约代码", "合约简称", "Delta", "Gamma", "Theta", "Vega", "隐含波动率", "权利金", "保证金"]
        return render(request, 'strategy.html', {'t_name': t_name, 'a': result[0], 'b': result[1], 'c': result[2],
                                                 'd': result[3]})
    elif request.method == "POST":
        strategy = request.POST.get('strategy')
        username = request.session.get('info')['username']
        # 生成交易单
        if strategy == "1":
            to.generate_transaction_order("48", "1", result[0][0], "1")
        elif strategy == "2":
            to.generate_transaction_order("50", "1", result[1][0], "1")
        elif strategy == "3":
            to.generate_transaction_order_two("1", result[2][0][0], result[2][1][0], "1")
        elif strategy == "4":
            to.generate_transaction_order_two("1", result[3][0][0], result[3][1][0], "1")
        # t_name = ["合约代码", "合约简称", "Delta", "Gamma", "Theta", "Vega", "隐含波动率", "权利金", "保证金"]
        update_strategy(username, strategy)
        return redirect('/profit/')
        # return render(request, 'success.html', {'strategy': strategy})


def update_strategy(username, strategy):
    date = time.strftime("%Y-%m-%d", time.localtime())
    if strategy == "1":
        up.add_strategy(username, "后市大涨", date, result[0])
    elif strategy == "2":
        up.add_strategy(username, "后市不跌", date, result[1])
    elif strategy == "3":
        up.add_strategy(username, "温涨", date, result[2])
    elif strategy == "4":
        up.add_strategy(username, "温涨坐庄", date, result[3])


def run():
    call_info = np.empty([0, 14], str)
    put_info = np.empty([0, 14], str)
    call_info, put_info = strategy_analyse.get_all_info()
    result = [strategy_analyse.rising_in_the_future(call_info),
              strategy_analyse.not_falling_in_the_future(put_info),
              strategy_analyse.temperature_rise(call_info),
              strategy_analyse.temperature_rise_sit(put_info)]
    return result



