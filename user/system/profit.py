from user import models
from django.shortcuts import render, redirect
import akshare as ak
import numpy as np
from decimal import Decimal


def show(request):
    username = request.session.get('info')['username']
    single_strategy = []
    composite_strategy = []
    single = models.SingleStrategy.objects.filter(username=username)
    composite = models.CompositeStrategy.objects.filter(username=username)
    if single.count() != 0:
        for info in single:
            now_price = float(np.asarray(ak.option_sse_spot_price_sina(info.option_code))[:, 1][2])
            if info.quantity != 0:
                if info.strategy_name == "后市大涨":
                    single_strategy.append(
                        [info.strategy_name, info.option_code, info.option_name, info.buy_sell, info.quantity, info.price,
                         now_price, Decimal(now_price - float(info.price)).quantize(Decimal("0.0000")),
                         Decimal((now_price - float(info.price)) / float(info.price) * 100).quantize(Decimal("0.00")),
                         info.date, info.time])
                else:
                    single_strategy.append(
                        [info.strategy_name, info.option_code, info.option_name, info.buy_sell, info.quantity, info.price,
                         now_price, Decimal(float(info.price) - now_price).quantize(Decimal("0.0000")),
                         Decimal((float(info.price) - now_price) / float(info.price) * 100).quantize(Decimal("0.00")),
                         info.date, info.time])

    if composite.count() != 0:
        for info in composite:
            if info.quantity_sell != 0 and info.quantity_buy != 0:
                now_price_buy = float(np.asarray(ak.option_sse_spot_price_sina(info.option_code_buy))[:, 1][2])
                now_price_sell = float(np.asarray(ak.option_sse_spot_price_sina(info.option_code_sell))[:, 1][2])
                composite_strategy.append(
                    [info.strategy_name, info.option_code_buy, info.option_name_buy, info.quantity_buy, info.price_buy,
                     now_price_buy, Decimal(now_price_buy - float(info.price_buy)).quantize(Decimal("0.0000")),
                     Decimal((now_price_buy - float(info.price_buy)) / float(info.price_buy) * 100).quantize(Decimal("0.00")),
                     info.option_code_sell, info.option_name_sell, info.quantity_sell, info.price_sell,now_price_sell,
                     Decimal(float(info.price_sell) - now_price_sell).quantize(Decimal("0.0000")),
                     Decimal((float(info.price_sell) - now_price_sell) / float(info.price_sell) * 100).quantize(Decimal("0.00")),
                     info.date, info.time])
    return render(request, 'profit.html', {'single': single_strategy, 'composite': composite_strategy})
