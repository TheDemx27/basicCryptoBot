# -*- coding: utf-8 -*-

import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import datetime as dt
import time
import ccxt
import requests  # noqa: E402
from scipy import optimize
import training as train
import getdata
from SMAstrat import SMAstrat

ftx_client = ccxt.ftx(config=json.load(open('config.json')))

def main():
    WINDOW = dt.timedelta(days=30)
    RES = 3600
    SYMBOL = 'GRT/USD'
    CB_SYMBOL = 'GRT-USD'

    usd_symbol = 'USD'
    b_symbol = 'GRT'

    while(True):
        """GET CURRENT DATA"""
        data = getdata.getHistPrice(WINDOW,RES,CB_SYMBOL)

        """TRAINING"""
        param = tuple([data])
        rrange = list(zip([1,2],[100,5]))

        ret = optimize.dual_annealing(train.f,args=param,bounds=rrange,maxiter=1000)

        """PLOTTING"""
        ind_SMAx = SMAstrat(data,ret.x[0],ret.x[1])
        print("30 DAY BACKTEST PERFORMANCE: " + str(ind_SMAx.profits))
        print("theta0 := " + str(ret.x[0]) + ", theta1 := " + str(ret.x[1]))

        plt.plot(ind_SMAx.data['close'])
        plt.plot(ind_SMAx.data['SMA_SHORT'])
        plt.plot(ind_SMAx.data['SMA_LONG'])
        plt.savefig('chart.png')

        """TRADING"""
        current_signal = ind_SMAx.currentSignal

        # GET BALANCES
        spread = getMarketPrice(ftx_client, SYMBOL)
        usd_balance, b_balance = getBalances(usd_symbol, b_symbol)
        
        if b_balance*spread['bid']>usd_balance:
            last_signal = 1
        else:
            last_signal = -1

        # LOGIC FOR PUTTING IN MARKET ORDERS
        if (current_signal != last_signal):
            if (current_signal == 1):
                print("MARKET BUY")
                ftx_client.create_market_buy_order(SYMBOL, usd_balance/spread['ask'])
            if (current_signal == -1):
                print("MARKET SELL")
                ftx_client.create_market_sell_order(SYMBOL, b_balance)
            last_signal = current_signal

        usd_balance, b_balance = getBalances(usd_symbol,b_symbol)
        print(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " ACCOUNT BALANCE: " + str(usd_balance) + " USD, " + str(b_balance) + " GRT")
        print("PORTFOLIO VALUE = " + str(usd_balance+b_balance*spread['bid']) + "\n")
        time.sleep(3600)
        plt.clf()

def getBalances(usd_symbol, b_symbol):
        balance = pd.DataFrame(ftx_client.fetch_balance())
        usd_balance = balance.loc[usd_symbol,'free']
        b_balance = balance.loc[b_symbol,'free']
        return (usd_balance,b_balance)

def getMarketPrice(exchange, symbol):
    orderbook = exchange.fetch_order_book(symbol)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    return { 'bid': bid, 'ask': ask, 'spread': spread }

if __name__ == "__main__":
    main()