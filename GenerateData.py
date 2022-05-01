# %%
from datetime import datetime
import nasdaqdatalink
import quandl
import yfinance as yf
import pandas as pd
from fredapi import Fred
import time
import json


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
    tf = open('data/meta_' + fileName + '.json', "w")
    json.dump(dict,tf)
    tf.close()
    
    with open('data/meta_' + fileName + '.js', 'w') as convert_file:
     convert_file.write('var meta = ')
     convert_file.write(json.dumps(dict))
     convert_file.write(';')


# %%
# Nasdaq Data
tickers_spRatio = {"MULTPL/SHILLER_PE_RATIO_MONTH" : 'Shiller PE Ratio',"MULTPL/SP500_DIV_YIELD_MONTH" : 'S&P500 Dividend Yield',"MULTPL/SP500_PE_RATIO_MONTH" : 'S&P 500 PE Ratio',"MULTPL/SP500_EARNINGS_YIELD_MONTH" : 'S&P 500 Earning Yield',"MULTPL/SP500_PBV_RATIO_QUARTER" : 'S&P 500 Price to Book Ratio',"MULTPL/SP500_PSR_QUARTER" : 'S&P 500 Price to Sales Ratio'}
tickers_worldInflationYoY = {"RATEINF/INFLATION_USA" : 'US Inflation',"RATEINF/INFLATION_GBR" : 'UK Inflation',"RATEINF/INFLATION_EUR" : 'Euro Area Inflation',"RATEINF/INFLATION_JPN" : 'Japan Inflation'}
tickers_allNasdaq = {**tickers_spRatio, **tickers_worldInflationYoY}

des = {"MULTPL/SHILLER_PE_RATIO_MONTH" : "Shiller PE ratio for the S&P 500. Price earnings ratio is based on average inflation-adjusted earnings from the previous 10 years, known as the Cyclically Adjusted PE Ratio (CAPE Ratio), Shiller PE Ratio, or PE 10 FAQ. Data courtesy of Robert Shiller from his book, Irrational Exuberance.",
       "MULTPL/SP500_DIV_YIELD_MONTH" : "S&P 500 dividend yield (12 month dividend per share)/price. Yields following March 2022 (including the current yield) are estimated based on 12 month dividends through March 2022, as reported by S&P. Sources: Standard & Poor's for current S&P 500 Dividend Yield. Robert Shiller and his book Irrational Exuberance for historic S&P 500 Dividend Yields.",
       "MULTPL/SP500_PE_RATIO_MONTH" : "Price to earnings ratio, based on trailing twelve month as reported earnings. Current PE is estimated from latest reported earnings and current market price. Source: Robert Shiller and his book Irrational Exuberance for historic S&P 500 PE Ratio.",
       "MULTPL/SP500_EARNINGS_YIELD_MONTH" : "S&P 500 Earnings Yield. Earnings Yield = trailing 12 month earnings divided by index price (or inverse PE) Yields following December, 2021 (including current yield) are estimated based on 12 month earnings through December, 2021 the latest reported by S&P. Source: Standard & Poor's",
       "MULTPL/SP500_PBV_RATIO_QUARTER" : "S&P 500 price to book value ratio. Current price to book ratio is estimated based on current market price and S&P 500 book value as of December, 2021 the latest reported by S&P. Source: Standard & Poor's",
       "MULTPL/SP500_PSR_QUARTER" : "S&P 500 Price to Sales Ratio (P/S or Price to Revenue). Current price to sales ratio is estimated based on current market price and 12 month sales ending December, 2021 the latest reported by S&P. Source: Standard & Poor's"}

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
        'des' : des.get(t,""),
        'source' : 'Nasdaq',
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
            'source' : 'Fred',
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


# %%
series = 'A191RL1Q225SBEA' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US Real GDP Growth (Percent Change from Preceding Period, SAAR)')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)



# %%
series = 'UNRATE' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US Unemployment Rate')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
series = 'PAYEMS' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'US Total Nonfarm')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)

print('Successfully download Fred data')

# %%
series = 'UMDMNO'
durableGoods = fred.get_series(series)
durableGoodsYOY = durableGoods.pct_change(periods=12)*100
durableGoodsYOY = durableGoodsYOY.dropna()
durableGoodsYOY_reset = durableGoodsYOY.reset_index()
durableGoodsYOY_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(durableGoodsYOY_reset, 'Date','Value')
meta = generateFredMeta(durableGoodsYOY_reset, series, 'US Durable Goods New Orders YoY')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)
