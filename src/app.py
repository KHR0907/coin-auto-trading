import pybithumb
import time
from datetime import datetime

all = pybithumb.get_current_price("ALL")
sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)

cycle_time = 1 # 초 간격으로 체크
loop_time = 60 * 120 # 초 동안 체크
ascent = 1 # % 상승

sec = 0
prev_ticker = ''
prev_rate = 0
prev_dict = { 'ticker' : 0 }

for ticker, data in sort_all :
    prev_dict[ticker] = data['fluctate_rate_24H']

while sec < loop_time :
    all = pybithumb.get_current_price("ALL")
    sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)

    for ticker, data in sort_all :
        diff = float(data['fluctate_rate_24H']) - float(prev_dict[ticker])
        if diff >= ascent :
            print(datetime.now(), ticker, data['closing_price'], data['fluctate_rate_24H'], float(prev_dict[ticker]), '%.2f' % diff )

        prev_dict[ticker] = data['fluctate_rate_24H']

    time.sleep(cycle_time)
    sec+=cycle_time

'''
'STRK': {'opening_price': '3177', 'closing_price': '3324', 'min_price': '3177', 'max_price': '3385',
         'units_traded': '3069590.83005712', 'acc_trade_value': '10072636308.2051', 'prev_closing_price': '3177',
         'units_traded_24H': '4509991.98179444', 'acc_trade_value_24H': '14573998715.6274', 'fluctate_24H': '198',
         'fluctate_rate_24H': '6.33'}}
'''

