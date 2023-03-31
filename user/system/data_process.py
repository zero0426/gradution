import json
from django.shortcuts import render, redirect, HttpResponse
import akshare as ak
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from tensorflow import keras
from django.views.decorators.csrf import csrf_exempt

"""
获取实时行情，并处理成便于展示的形式


"""


def get_sz_date_info(symbol, date, exchange):
    """
    获取指定交易所，指定到期月份，指定期权类型的全部合约代码
    :param symbol: 期权类型，"看涨期权"或者"看跌期权"
    :param date: 前四位为年份，后两位为月份，如 "202303"
    :param exchange: 期权所属交易所代码，上交所50ETF为 "510050"
    :return: 返回所有符合条件的合约代码，四列分别为[期权类型,交易所代码,到期月份,合约代码]
    """
    code = np.empty([0, 4])
    x = np.asarray(ak.option_sse_codes_sina(symbol, date, exchange))
    y = np.empty([x.shape[0], x.shape[1]], str)
    x = np.concatenate((y, x), axis=1)
    code = np.concatenate((code, x))
    code[:, 0] = symbol
    code[:, 1] = exchange
    code[:, 2] = date
    return code


def get_sz_info_list(code):
    """
    获取指定合约代码的实时信息
    :param code: 含有多个合约代码的numpy数组
    :return: 详细信息数组
    """
    info_list = np.empty([43, 0])
    for c in code:
        info = np.delete(np.asarray(ak.option_sse_spot_price_sina(c[3])), 0, 1)
        info_list = np.concatenate((info_list, info), axis=1)
    info_list = np.transpose(info_list)
    info_list = np.concatenate((code, info_list), axis=1)
    return info_list


def quotes(request):
    """
    第一次打开查看行情网页，默认返回最近的到期月份的期权的实时行情
    :param request:
    :return: 最近到期月份的期权的实时行情
    """
    date = ak.option_sse_list_sina()
    # call_code = get_sz_date_info("看涨期权", date[0], "510050")
    # call_info_list = get_sz_info_list(call_code)
    # put_code = get_sz_date_info("看跌期权", date[0], "510050")
    # put_info_list = get_sz_info_list(put_code)
    return redirect('/quotes/'+date[0]+'/')
    # return render(request, 'quotes.html',
    #               {'date': date, 'call_info_list': call_info_list, 'put_info_list': put_info_list, 'now': date[0]})


def quotes_month(request, month):
    """
    查看指定到期月份期权的行情
    :param request:
    :param month: 查看到期月份
    :return: 所查看的到期月份的期权实时行情
    """
    date = ak.option_sse_list_sina()
    call_code = get_sz_date_info("看涨期权", month, "510050")
    call_info_list = get_sz_info_list(call_code)
    put_code = get_sz_date_info("看跌期权", month, "510050")
    put_info_list = get_sz_info_list(put_code)
    return render(request, 'quotes.html',
                  {'date': date, 'call_info_list': call_info_list, 'put_info_list': put_info_list, 'now': month})


def refresh(request):
    month = request.GET.get('month')
    call_code = get_sz_date_info("看涨期权", month, "510050")
    call_info_list = get_sz_info_list(call_code).tolist()
    put_code = get_sz_date_info("看跌期权", month, "510050")
    put_info_list = get_sz_info_list(put_code).tolist()
    data = {'call_info_list': call_info_list, 'put_info_list': put_info_list}
    return HttpResponse(json.dumps(data))


def train(fund_id, num, step):
    """

    :param fund_id: 基金代码
    :param num: 训练集大小
    :param step: 预测未来天数
    :return:
    """
    data = ak.fund_open_fund_info_em(fund_id)
    training_set = data.iloc[data.shape[0] - num - step:, 1:2].values
    X_train = training_set[0:num]
    Y_train = training_set[step:num + step]
    X_train = np.reshape(X_train, (num, 1, 1))
    regressor = Sequential()
    regressor.add(LSTM(units=50, activation='sigmoid', input_shape=(1, 1)))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error')
    regressor.fit(X_train, Y_train, batch_size=32, epochs=100)
    regressor.save('model.h5')
    print("训练成功")


def predict(num):
    data = ak.fund_open_fund_info_em('510050')
    model = keras.models.load_model('model.h5')
    inputs = data.iloc[data.shape[0] - num:, 1:2].values
    inputs = np.reshape(inputs, (num, 1, 1))
    predicted_price = model.predict(inputs)
    return predicted_price


def update_daily_info():
    date = ak.option_sse_list_sina()
    for month in date:

        call_code = get_sz_date_info("看涨期权", date[0], "510050")
        call_info_list = get_sz_info_list(call_code)
        put_code = get_sz_date_info("看跌期权", date[0], "510050")
        put_info_list = get_sz_info_list(put_code)



