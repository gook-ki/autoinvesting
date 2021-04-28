import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_price2(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    dft = pyupbit.get_ohlcv(ticker, interval="day", count=1)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    target_price2 = dft.iloc[0]['high'] * 0.93
    return target_price2

def nowprice(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    dft = pyupbit.get_ohlcv(ticker, interval="day", count=1)  #시가, 고가, 저가, 종가(당일 현재가), 거래량
    now_price = dft.iloc[0]['close']
    return now_price




def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-NEO") # 9:00
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price2 = get_target_price2("KRW-NEO")
            target_price = get_target_price("KRW-NEO", 0.8)
            current_price = get_current_price("KRW-NEO")
            now_price=nowprice("KRW-NEO")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-NEO", krw*0.9995)
            if now_price < target_price2:
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
