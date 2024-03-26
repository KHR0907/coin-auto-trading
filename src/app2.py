import pybithumb
import time
from datetime import datetime

all = pybithumb.get_current_price("ALL")
sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)

cycle_time = 10  # 초 간격으로 체크
sell_cycle_time = 1  # 파는 간격을 초 간격으로 체크
loop_time = 60 * 120  # 초 동안 체크
ascent = 0.1  # % 상승
sell_ascent = 0.3  # 매수후 % 상승 후 매도

buy_flag = False
sec = 0
prev_dict = {'ticker': 0}

for ticker, data in sort_all:
    prev_dict[ticker] = data['fluctate_rate_24H']

# 사기 로직
while sec < loop_time and buy_flag == False:
    all = pybithumb.get_current_price("ALL")
    sort_all = sorted(all.items(), key=lambda x: float(x[1]['fluctate_rate_24H']), reverse=True)

    for ticker, data in sort_all:
        diff = float(data['fluctate_rate_24H']) - float(prev_dict[ticker])
        if diff >= ascent:
            buy = [str(datetime.now()), ticker, float(data['closing_price']), float(data['fluctate_rate_24H']),
                   float(prev_dict[ticker]), float('%.2f' % diff)]
            print('BUY ', buy)
            buy_flag = True
            break;

        prev_dict[ticker] = data['fluctate_rate_24H']

    time.sleep(cycle_time)
    sec += cycle_time

# 팔기 로직
sell_flag = False

while sell_flag == False:
    current_price = pybithumb.get_current_price(buy[1])
    yield_rate = (current_price - float(buy[2])) / float(buy[2]) * 100

    # print ( current_price , float (buy[2]), '%.2f' % yield_rate )
    if (yield_rate >= sell_ascent):
        sell = [str(datetime.now()), buy[1], current_price, float(buy[2]), float('%.2f' % yield_rate)]
        print('SELL', sell)
        sell_flag = True

    time.sleep(1)