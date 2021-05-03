import time
import pyupbit
import datetime

access = ""          # 본인 값으로 변경
secret = ""          # 본인 값으로 변경



def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    target_price = df.iloc[0]['low'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_price2(ticker,kk):
    dft = pyupbit.get_ohlcv(ticker, interval="day", count=1)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    target_price2 = dft.iloc[0]['high'] * kk
    return target_price2


def highprice(ticker):
    dft = pyupbit.get_ohlcv(ticker, interval="day", count=1)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    high_price = dft.iloc[0]['high']
    return high_price

def openprice(ticker):
    dft = pyupbit.get_ohlcv(ticker, interval="day", count=1)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    openp = dft.iloc[0]['open']
    return openp


def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

buyprice = 0;

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-NEO") # 9:00
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=3):
            target_price = get_target_price("KRW-NEO", 0.8)
            current_price = get_current_price("KRW-NEO")
            high_price = highprice("KRW-NEO")
            open_price = openprice("KRW-NEO")



            if target_price < current_price and high_price*0.99 < current_price :
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-NEO", krw*0.9995)
                    buyprice = max(target_price, open_price, high_price*0.99)

            if buyprice > 0:
                if buyprice + 500 < current_price < high_price * 0.98: #earn profit
                    NEO = get_balance("NEO")
                    if NEO > 0.05:
                        upbit.sell_market_order("KRW-NEO", NEO * 0.9995)

                if current_price < buyprice * 0.98:         # limit loss
                    NEO = get_balance("NEO")
                    if NEO > 0.05:
                        upbit.sell_market_order("KRW-NEO", NEO * 0.9995)

        else:
            NEO = get_balance("NEO")
            if NEO > 0.05:
                upbit.sell_market_order("KRW-NEO", NEO*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
