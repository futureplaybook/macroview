# %%
from datetime import datetime
import nasdaqdatalink
import quandl
import yfinance as yf
import pandas as pd
from fredapi import Fred


# %%
import json


def GenerateHighchartVar(df, fieldX, fieldY):
    df.reset_index()
    init = '[' + '\n'
    s = ''
    
    for i in range(len(df)):
        s = s + '[' + str(df.loc[i, fieldX].timestamp() * 1000) + ',' + str(df.loc[i, fieldY]) + '],' + '\n'
    
    s = s[:-2]
    s = init + s + "]"
    
    return s

def generateJSONDataFile(fileName, content):
    with open("data/data_" + fileName+ ".json", "w") as outfile:
        outfile.write(content)
        
def generateMetadataFile(dict, fileName):
    with open('data/meta_' + fileName + '.js', 'w') as convert_file:
     convert_file.write('var meta = ')
     convert_file.write(json.dumps(dict))
     convert_file.write(';')



# %%
# Yahoo Data
# https://www.ssga.com/library-content/products/fund-docs/etfs/us/information-schedules/spdr-etf-listing.pdf
tickers_WorldIndex = ['^GSPC','^DJI','^IXIC','^RUT','^VIX','^FTSE','^N225','^HSI']
tickers_ccy = ['DX-Y.NYB', 'EURUSD=X','JPY=X','GBPUSD=X', 'AUDUSD=X', 'NZDUSD=X','CNY=X','CAD=X']
tickers_commodities = ['GC=F','SI=F','CL=F']
tickers_treasury = ['ZT=F','ZN=F','ZB=F']

tickers_sector = ['XLC','XLP','XLY','XLE','XLF','XLV','XLI','XLB','XLRE','XLK','XLU']
tickers_style = ['SPTM','SPLG','SPMD','SPSM','SPYG','SPYV','SPYD']

tickers_yahoo = tickers_WorldIndex+tickers_ccy+tickers_commodities+tickers_treasury+tickers_sector+tickers_style


asOfDateTime = datetime.now()
asOfDateTimeStr = asOfDateTime.strftime("%d/%m/%Y %H:%M:%S")

for t in tickers_yahoo:
    name = t.replace('^','').replace('=F','').replace('=X','').replace('DX-Y.NYB','DXY')
    rawData = yf.download(t)
    #indexedData = rawData['Adj Close'].tail(950).reset_index()
    indexedData = rawData['Adj Close'].reset_index()
    indexedData.columns = ['Date','Value']
    highChartTS = GenerateHighchartVar(indexedData, 'Date','Value')
    generateJSONDataFile(name, highChartTS)
    
    meta = {'name': name,
        'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%y'),
        'currentValue' : indexedData.tail(1)['Value'].item(),
        'minDate' : (indexedData.min()['Date']).strftime('%d-%m-%y'),
        'minValue' : indexedData.min()['Value'],
        'maxDate' : (indexedData.max()['Date']).strftime('%d-%m-%y'),
        'maxValue' : indexedData.max()['Value'],
        'lastUpdate' : asOfDateTimeStr,
        'dataFilename' : '/macroview/data/data_' + name + '.json'
        }
    
    generateMetadataFile(meta, name)

# %%
# Nasdaq Data
tickers_spRatio = ["MULTPL/SHILLER_PE_RATIO_MONTH","MULTPL/SP500_DIV_YIELD_MONTH","MULTPL/SP500_PE_RATIO_MONTH","MULTPL/SP500_EARNINGS_YIELD_MONTH","MULTPL/SP500_PBV_RATIO_QUARTER","MULTPL/SP500_PSR_QUARTER"]
tickers_worldInflationYoY = ["RATEINF/INFLATION_USA","RATEINF/INFLATION_GBR","RATEINF/INFLATION_EUR","RATEINF/INFLATION_JPN"]

tickers_allNasdaq = tickers_spRatio + tickers_worldInflationYoY

asOfDateTime = datetime.now()
asOfDateTimeStr = asOfDateTime.strftime("%d/%m/%Y %H:%M:%S")

for t in tickers_allNasdaq:
    rawData = quandl.get(t, authtoken="cza_RyNfSzs9o1Z2QBs4")
    #indexedData = rawData.tail(950).reset_index()
    indexedData = rawData.reset_index()
    highChartTS = GenerateHighchartVar(indexedData, 'Date','Value')
    generateJSONDataFile(t.replace('/','_'), highChartTS)
    
    meta = {'name': t.replace('/','_'),
        'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%Y'),
        'currentValue' : indexedData.tail(1)['Value'].item(),
        'minDate' : (indexedData.min()['Date']).strftime('%d-%m-%Y'),
        'minValue' : indexedData.min()['Value'],
        'maxDate' : (indexedData.max()['Date']).strftime('%d-%m-%Y'),
        'maxValue' : indexedData.max()['Value'],
        'lastUpdate' : asOfDateTimeStr,
        'dataFilename' : '/macroview/data/data_' + t.replace('/','_') + '.json'
        }
    
    generateMetadataFile(meta, t.replace('/','_'))




# %%
# Fred Data

fred = Fred(api_key='d79cebb1e12819cd44ed96cc291f0f72')

def generateFredMeta(indexedData, name = ''):
    asOfDateTime = datetime.now()
    asOfDateTimeStr = asOfDateTime.strftime("%d/%m/%Y %H:%M:%S")
    meta = {'name': name,
            'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%y'),
            'currentValue' : indexedData.tail(1)['Value'].item(),
            'minDate' : (indexedData.min()['Date']).strftime('%d-%m-%y'),
            'minValue' : indexedData.min()['Value'],
            'maxDate' : (indexedData.max()['Date']).strftime('%d-%m-%y'),
            'maxValue' : indexedData.max()['Value'],
            'lastUpdate' : asOfDateTimeStr,
            'dataFilename' : '/macroview/data/data_' + name + '.json'
            }
    return meta

# %%
coreCPI = fred.get_series('CPILFESL')
coreCPIYOY = coreCPI.pct_change(periods=12)*100
coreCPIYOY = coreCPIYOY.dropna()
coreCPIYOY_reset = coreCPIYOY.reset_index()
coreCPIYOY_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(coreCPIYOY_reset, 'Date','Value')
meta = generateFredMeta(coreCPIYOY_reset, 'coreCPIYOY')
generateMetadataFile(meta, 'coreCPIYOY')
generateJSONDataFile('coreCPIYOY', highChartTS)

# %%
headlineCPI = fred.get_series('CPIAUCSL')
headlineCPIYOY = headlineCPI.pct_change(periods=12)*100
headlineCPIYOY = headlineCPIYOY.dropna()
headlineCPIYOY_reset = headlineCPIYOY.reset_index()
headlineCPIYOY_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(headlineCPIYOY_reset, 'Date','Value')
meta = generateFredMeta(headlineCPIYOY_reset, 'headlineCPIYOY')
generateMetadataFile(meta, 'headlineCPIYOY')
generateJSONDataFile('headlineCPIYOY', highChartTS)

# %%
#10y2y yield spread
series = 'T10Y2Y' 
df = fred.get_series(series)
df_reset = df.reset_index()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, '10y2y Yield Spread')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
#Real Yield
series = 'DFII10' 
df = fred.get_series(series)
df_reset = df.reset_index()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, 'Real Yield')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)



# %%
#Nominal Yield
series = 'DGS10' 
df = fred.get_series(series)
df_reset = df.reset_index()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, 'Nominal Yield')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
#Breakeven Rate
series = 'T10YIE' 
df = fred.get_series(series)
df_reset = df.reset_index()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, 'Breakeven Rate')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)

