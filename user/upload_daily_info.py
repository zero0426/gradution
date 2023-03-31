import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'options_strategy_trading_system.settings')
django.setup()

from user import models
from user.system import data_process
import akshare as ak
from decimal import Decimal

def upload():
    print("start update daily info")
    months = ak.option_sse_list_sina()
    for month in months:
        call_code = data_process.get_sz_date_info("看涨期权", month, "510050")
        call_info_list = data_process.get_sz_info_list(call_code)
        for call_info in call_info_list:
            info = models.option_daily_info(option_code=call_info[3], option_name=call_info[41],
                                            date=call_info[36][0:10],
                                            open_price=float(call_info[13]), close_price=float(call_info[6]),
                                            highest_price=float(call_info[43]), lowest_price=float(call_info[44]),
                                            transaction_num=int(call_info[45]), turnover=Decimal(float(call_info[46])).quantize(Decimal("0.0000")))
            old_info = models.option_daily_info.objects.filter(option_code=info.option_code, date=info.date).first()
            if old_info is not None:
                # 数据库中已有信息,更新信息
                old_info.close_price = info.close_price
                old_info.highest_price = info.highest_price
                old_info.lowest_price = info.lowest_price
                old_info.transaction_num = info.transaction_num
                old_info.turnover = info.turnover
                old_info.save()
            else:
                info.save()
        put_code = data_process.get_sz_date_info("看跌期权", month, "510050")
        put_info_list = data_process.get_sz_info_list(put_code)
        for put_info in put_info_list:
            info = models.option_daily_info(option_code=put_info[3], option_name=put_info[41],
                                            date=put_info[36][0:10],
                                            open_price=float(put_info[13]), close_price=float(put_info[6]),
                                            highest_price=float(put_info[43]), lowest_price=float(put_info[44]),
                                            transaction_num=int(put_info[45]), turnover=Decimal(float(put_info[46])).quantize(Decimal("0.0000")))
            old_info = models.option_daily_info.objects.filter(option_code=info.option_code, date=info.date).first()
            if old_info is not None:
                # 数据库中已有信息,更新信息
                old_info.close_price = info.close_price
                old_info.highest_price = info.highest_price
                old_info.lowest_price = info.lowest_price
                old_info.transaction_num = info.transaction_num
                old_info.turnover = info.turnover
                old_info.save()
            else:
                info.save()
    print("daily info update success")

upload()