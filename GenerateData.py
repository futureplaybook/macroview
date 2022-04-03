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
tickers_WorldIndex = {'^GSPC' : 'SP500','^DJI' : 'Dow Jones','^IXIC' : 'Nasdaq','^RUT' : 'Russell 2000','^VIX' : 'VIX','^FTSE' : 'FTSE 100','^N225' : 'Nikkei 225','^HSI' : 'Hang Seng Index'}
tickers_ccy = {'DX-Y.NYB' : 'USD', 'EURUSD=X' : 'EURUSD','JPY=X' : 'USDJPY','GBPUSD=X' : 'GBPUSD', 'AUDUSD=X' : 'AUDUSD', 'NZDUSD=X' : 'NZDUSD','CNY=X' : 'CNY','CAD=X' : 'USDCAD'}
tickers_commodities = {'GC=F' : 'Gold','SI=F' : 'Silver','CL=F' : 'Crude'}
tickers_treasury = {'ZT=F' : 'US 2-Year Note','ZN=F' : 'US 10-Year Note','ZB=F' : 'US Treasury'}

tickers_sector = {'XLC' : 'Communication Service','XLP' : 'Consumer Staples','XLY' : 'Consumer Discretionary','XLE' : 'Energy','XLF' : 'Financial','XLV' : 'Health Care','XLI' : 'Industrial','XLB' : 'Materials','XLRE' : 'Real Estate','XLK' : 'Technology','XLU' : 'Utilities'}
tickers_style = {'SPTM' : 'SP 1500','SPLG' : 'Large Cap','SPMD' : 'Mid Cap','SPSM'  : 'Small Cap','SPYG'  : 'Growth','SPYV' : 'Value','SPYD' : 'High Dividend Yield'}

tickers_yahoo = {**tickers_WorldIndex, **tickers_ccy, **tickers_commodities, **tickers_treasury, **tickers_sector, **tickers_style}


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
            'displayName': tickers_yahoo[t],
            'dataFrom': (indexedData.head(1)['Date'].item()).strftime('%m/%Y'),
            'dataTo': (indexedData.tail(1)['Date'].item()).strftime('%m/%Y'),
        'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%Y'),
        'currentValue' : indexedData.tail(1)['Value'].item(),
        'minDate' : (indexedData.iloc[indexedData['Value'].idxmin(),:]['Date']).strftime('%d-%m-%Y'),
        'minValue' : indexedData.min()['Value'],
        'maxDate' : (indexedData.iloc[indexedData['Value'].idxmax(),:]['Date']).strftime('%d-%m-%Y'),
        'maxValue' : indexedData.max()['Value'],
        'lastUpdate' : asOfDateTimeStr,
        'dataFilename' : '/macroview/data/data_' + name + '.json'
        }
    
    generateMetadataFile(meta, name)
    
print('Successfully download Yahoo data')

# %%
# Nasdaq Data
tickers_spRatio = {"MULTPL/SHILLER_PE_RATIO_MONTH" : 'Shiller PE Ratio',"MULTPL/SP500_DIV_YIELD_MONTH" : 'S&P500 Dividend Yield',"MULTPL/SP500_PE_RATIO_MONTH" : 'S&P 500 PE Ratio',"MULTPL/SP500_EARNINGS_YIELD_MONTH" : 'S&P 500 Earning Yield',"MULTPL/SP500_PBV_RATIO_QUARTER" : 'S&P 500 Price to Book Ratio',"MULTPL/SP500_PSR_QUARTER" : 'S&P 500 Price to Sales Ratio'}
tickers_worldInflationYoY = {"RATEINF/INFLATION_USA" : 'US Inflation',"RATEINF/INFLATION_GBR" : 'UK Inflation',"RATEINF/INFLATION_EUR" : 'Euro Area Inflation',"RATEINF/INFLATION_JPN" : 'Japan Inflation'}

tickers_allNasdaq = {**tickers_spRatio, **tickers_worldInflationYoY}

asOfDateTime = datetime.now()
asOfDateTimeStr = asOfDateTime.strftime("%d/%m/%Y %H:%M:%S")

for t in tickers_allNasdaq:
    rawData = quandl.get(t, authtoken="cza_RyNfSzs9o1Z2QBs4")
    #indexedData = rawData.tail(950).reset_index()
    indexedData = rawData.reset_index()
    highChartTS = GenerateHighchartVar(indexedData, 'Date','Value')
    generateJSONDataFile(t.replace('/','_'), highChartTS)
    
    meta = {'name': t.replace('/','_'),
            'displayName': tickers_allNasdaq[t],
            'dataFrom': (indexedData.head(1)['Date'].item()).strftime('%m/%Y'),
            'dataTo': (indexedData.tail(1)['Date'].item()).strftime('%m/%Y'),
        'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%Y'),
        'currentValue' : indexedData.tail(1)['Value'].item(),
        'minDate' : (indexedData.iloc[indexedData['Value'].idxmin(),:]['Date']).strftime('%d-%m-%Y'),
        'minValue' : indexedData.min()['Value'],
        'maxDate' : (indexedData.iloc[indexedData['Value'].idxmax(),:]['Date']).strftime('%d-%m-%Y'),
        'maxValue' : indexedData.max()['Value'],
        'lastUpdate' : asOfDateTimeStr,
        'dataFilename' : '/macroview/data/data_' + t.replace('/','_') + '.json'
        }
    
    generateMetadataFile(meta, t.replace('/','_'))


print('Successfully download Nasdaq data')



# %%
# Fred Data

fred = Fred(api_key='d79cebb1e12819cd44ed96cc291f0f72')

def generateFredMeta(indexedData, name = '', displayName = ''):
    asOfDateTime = datetime.now()
    asOfDateTimeStr = asOfDateTime.strftime("%d/%m/%Y %H:%M:%S")
    meta = {'name': name,
            'displayName': displayName,
            'dataFrom': (indexedData.head(1)['Date'].item()).strftime('%m/%Y'),
            'dataTo': (indexedData.tail(1)['Date'].item()).strftime('%m/%Y'),
            'currentUpdate': (indexedData.tail(1)['Date'].item()).strftime('%d-%m-%Y'),
            'currentValue' : indexedData.tail(1)['Value'].item(),
            'minDate' : (indexedData.iloc[indexedData['Value'].idxmin(),:]['Date']).strftime('%d-%m-%Y'),
            'minValue' : indexedData.min()['Value'],
            'maxDate' : (indexedData.iloc[indexedData['Value'].idxmax(),:]['Date']).strftime('%d-%m-%Y'),
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
meta = generateFredMeta(coreCPIYOY_reset, 'coreCPIYOY', 'US Core CPI')
generateMetadataFile(meta, 'coreCPIYOY')
generateJSONDataFile('coreCPIYOY', highChartTS)

# %%
headlineCPI = fred.get_series('CPIAUCSL')
headlineCPIYOY = headlineCPI.pct_change(periods=12)*100
headlineCPIYOY = headlineCPIYOY.dropna()
headlineCPIYOY_reset = headlineCPIYOY.reset_index()
headlineCPIYOY_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(headlineCPIYOY_reset, 'Date','Value')
meta = generateFredMeta(headlineCPIYOY_reset, 'headlineCPIYOY', 'US Headline CPI')
generateMetadataFile(meta, 'headlineCPIYOY')
generateJSONDataFile('headlineCPIYOY', highChartTS)

# %%
#10y2y yield spread
series = 'T10Y2Y' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US 10-2 Year Treasury Yield Spread')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
#Real Yield
series = 'DFII10' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US Real Yield')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)



# %%
#Nominal Yield
series = 'DGS10' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US Nominal Yield')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
#Breakeven Rate
series = 'T10YIE' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US 10-Year Breakeven Inflation Rate')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)

print('Successfully download Fred data')

