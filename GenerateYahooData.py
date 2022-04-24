import time
from random import randint
from retrying import retry
from pebble import concurrent

from datetime import datetime
import nasdaqdatalink
import quandl
import yfinance as yf
import pandas as pd
from fredapi import Fred
import time
import math
import json

class TimeoutException(Exception):
    pass

def GenerateHighchartVar(df, fieldX, fieldY):
    df.dropna(how='any')
    init = '[' + '\n'
    s = ''
    #print(df)
    for i in range(len(df)):
        if math.isnan(df.loc[i, fieldY]) == False:
            s = s + '[' + str(df.loc[i, fieldX].timestamp() * 1000) + ',' + str(df.loc[i, fieldY]) + '],' + '\n'
    
    s = s[:-2]
    s = init + s + "]"
    
    return s

def generateJSONDataFile(fileName, content):
    with open("data/data_" + fileName+ ".json", "w") as outfile:
        outfile.write(content)
        
def generateMetadataFile(dict, fileName):
    tf = open('data/meta_' + fileName + '.json', "w")
    json.dump(dict,tf)
    tf.close()
    
    with open('data/meta_' + fileName + '.js', 'w') as convert_file:
     convert_file.write('var meta = ')
     convert_file.write(json.dumps(dict))
     convert_file.write(';')


# Yahoo Data
# https://www.ssga.com/library-content/products/fund-docs/etfs/us/information-schedules/spdr-etf-listing.pdf
@concurrent.process(timeout=30)
def getYahooData(tickerDict):
    asOfDateTime = datetime.now()
    asOfDateTimeStr = asOfDateTime.strftime("%d/%m/%Y %H:%M:%S")

    tickerList = list(tickerDict.keys())
    d = yf.download(tickerList)
    rawData = d['Adj Close'].reset_index()
    print('Successfully download Yahoo data')

    for t in tickerList:
        name = t.replace('^','').replace('=F','').replace('=X','').replace('DX-Y.NYB','DXY')
        #rawData = yf.download(t)
        #indexedData = rawData['Adj Close'].tail(950).reset_index()
        indexedData = rawData[['Date',t]]
        
        #indexedData = rawData['Adj Close'].reset_index()
        indexedData.columns = ['Date','Value']
        highChartTS = GenerateHighchartVar(indexedData, 'Date','Value')
        generateJSONDataFile(name, highChartTS)
        
        meta = {'name': name,
                'displayName': tickerDict[t],
                'dataFrom': (indexedData.head(1)['Date'].item()).strftime('%m/%Y'),
                'dataTo': (indexedData.tail(1)['Date'].item()).strftime('%m/%Y'),
            'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%Y'),
            'currentValue' : indexedData.tail(1)['Value'].item(),
            'minDate' : (indexedData.iloc[indexedData['Value'].idxmin(),:]['Date']).strftime('%d-%m-%Y'),
            'minValue' : indexedData.min()['Value'],
            'maxDate' : (indexedData.iloc[indexedData['Value'].idxmax(),:]['Date']).strftime('%d-%m-%Y'),
            'maxValue' : indexedData.max()['Value'],
            'lastUpdate' : asOfDateTimeStr,
            'source' : 'Internet',
            'dataFilename' : '/macroview/data/data_' + name + '.json'
            }
        
        generateMetadataFile(meta, name)
        print('Done ' + name)
    




@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_1():
    tickers_WorldIndex = {'^GSPC' : 'SP500', 
                '^DJI' : 'Dow Jones', 
                '^IXIC' : 'Nasdaq', 
                '^RUT' : 'Russell 2000', 
                '^VIX' : 'VIX', 
                '^FTSE' : 'FTSE 100',
                '^STOXX' : 'STOXX 600', 
                '^FCHI' : 'CAC 40', 
                '^GDAXI' : 'DAX', 
                '^IBEX' : 'IBEX 35', 
                '^N225' : 'Nikkei 225', 
                '000001.SS' : 'Shanghai Stock Exchange Composite Index',
                '^KS11' : 'KOSPI Composite Index',
                '^HSI' : 'Hang Seng Index'}
    
    result = getYahooData(tickers_WorldIndex).result()  # blocks until results are ready

@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_2():
    tickers_ccy = {'DX-Y.NYB' : 'USD', 'EURUSD=X' : 'EURUSD','JPY=X' : 'USDJPY','GBPUSD=X' : 'GBPUSD', 'AUDUSD=X' : 'AUDUSD', 'NZDUSD=X' : 'NZDUSD','CNY=X' : 'CNY','CAD=X' : 'USDCAD'}
    result = getYahooData(tickers_ccy).result()  # blocks until results are ready
    
@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_3():
    tickers_commodities = {'GC=F' : 'Gold', 'SI=F' : 'Silver', 'CL=F' : 'Crude oil', 'ALI=F' : 'Aluminum', 'HG=F' : 'Copper', 'NG=F' : 'Natural Gas'}
    result = getYahooData(tickers_commodities).result()

@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_4():
    tickers_treasury = {'ZT=F' : 'US 2-Year Note', 'ZN=F' : 'US 10-Year Note', 'ZB=F' : 'US Treasury'}
    result = getYahooData(tickers_treasury).result()
    
@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_5():
    tickers_sector = {'XLC' : 'Communication Service (XLC)', 'XLP' : 'Consumer Staples (XLP)', 'XLY' : 'Consumer Discretionary (XLY)', 'XLE' : 'Energy (XLE)', 'XLF' : 'Financial (XLF)', 'XLV' : 'Health Care (XLV)', 'XLI' : 'Industrial (XLI)', 'XLB' : 'Materials (XLB)', 'XLRE' : 'Real Estate (XLRE)', 'XLK' : 'Technology (XLK)', 'XLU' : 'Utilities (XLU)'}
    result = getYahooData(tickers_sector).result()

@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_6():
    tickers_style = {'SPTM' : 'SP 1500','SPLG' : 'Large Cap','SPMD' : 'Mid Cap','SPSM'  : 'Small Cap','SPYG'  : 'Growth','SPYV' : 'Value','SPYD' : 'High Dividend Yield'}
    result = getYahooData(tickers_style).result()

@retry(stop_max_attempt_number=5)  # stop after 6 attempts
def function_7():
    tickers_arg = {'LE=F' : 'Live Cattle', 'KC=F' : 'Coffee', 'ZC=F' : 'Corn', 'CT=F' : 'Cotton', 'ZS=F': 'Soybean', 'SB=F' : 'Sugar', 'ZW=F' : 'Wheat'} 
    result = getYahooData(tickers_arg).result()
    


if __name__ == "__main__":
    try:
        function_1()
        function_2()
        function_3()
        function_4()
        function_5()
        function_6()
        function_7()
    except Exception as error:
        print("Timeout! %s" % error)