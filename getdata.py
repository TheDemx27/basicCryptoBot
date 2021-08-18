import datetime as dt
import Historic_Crypto as hc
import csv

def getHistPrice(window, res, sym):
    startstr = (dt.datetime.utcnow() - window).strftime('%Y-%m-%d-%H-%M')
    endstr = dt.datetime.utcnow().strftime('%Y-%m-%d-%H-%M')

    return hc.HistoricalData(sym,res,startstr,endstr,verbose=False).retrieve_data().reset_index()