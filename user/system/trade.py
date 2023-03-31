import requests
import akshare as ak
from user import models
import numpy as np


def buy(option_code, username, num):
    option_info = np.asarray(ak.option_sse_spot_price_sina(option_code))
    transaction = models.Transaction(username=username, option_code=option_code, buy_sell="买", quantity=num,price=option_info[20])
    transaction.save()
    option = models.Option(username=username, option_code=option_code,option_name=option_info[37],buy_sell="买",position_volume=num,open_price=option_info[20])
    option.save()


def sell(option_id, username, num):
    pass