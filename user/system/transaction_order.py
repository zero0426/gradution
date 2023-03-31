import shutil
import time

def generate_transaction_order(transaction_type, access, option_code, num):
    """

    :param transaction_type: 交易类型 买入开仓：48   卖出平仓：49
                                    卖出开仓：50   买入平仓：51
                                    认购行权：54   认沽行权：55
    :param access: 通道号
    :param option_code: 期权代码
    :param num: 交易数量
    :return:
    """

    msg = transaction_type + "," + access + ",," + option_code + "," + num + "\n"
    path = r'D:\Project\options_strategy_trading_system\input.txt'
    file = open(path, 'a')
    file.write(msg)
    file.close()
    new_path = r'D:\Project\options_strategy_trading_system\input'
    shutil.move(path, new_path)
    time.sleep(5)


def generate_transaction_order_two(access, option_code_buy,option_code_sell, num):
    msg_buy = "48" + "," + access + ",," + option_code_buy + "," + num + "\n"
    msg_sell = "50" + "," + access + ",," + option_code_sell + "," + num + "\n"
    path = r'D:\Project\options_strategy_trading_system\input.txt'
    file = open(path, 'a')
    file.write(msg_buy)
    file.write(msg_sell)
    file.close()
    new_path = r'D:\Project\options_strategy_trading_system\input'
    shutil.move(path, new_path)
    time.sleep(5)
