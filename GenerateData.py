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

def generateFredMeta(indexedData, name = '', displayName = '', des = ' '):
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
            'des' : des,
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
des = 'The "Consumer Price Index for All Urban Consumers: All Items Less Food & Energy" is an aggregate of prices paid by urban consumers for a typical basket of goods, excluding food and energy. This measurement, known as "Core CPI," is widely used by economists because food and energy have very volatile prices. The Bureau of Labor Statistics defines and measures the official CPI'
meta = generateFredMeta(coreCPIYOY_reset, 'coreCPIYOY', 'US Core CPI', des)
generateMetadataFile(meta, 'coreCPIYOY')
generateJSONDataFile('coreCPIYOY', highChartTS)

# %%
headlineCPI = fred.get_series('CPIAUCSL')
headlineCPIYOY = headlineCPI.pct_change(periods=12)*100
headlineCPIYOY = headlineCPIYOY.dropna()
headlineCPIYOY_reset = headlineCPIYOY.reset_index()
headlineCPIYOY_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(headlineCPIYOY_reset, 'Date','Value')
des = 'The Consumer Price Index for All Urban Consumers: All Items (CPIAUCSL) is a price index of a basket of goods and services paid by urban consumers. Percent changes in the price index measure the inflation rate between any two time periods. The most common inflation metric is the percent change from one year ago. It can also represent the buying habits of urban consumers. This particular index includes roughly 88 percent of the total population, accounting for wage earners, clerical workers, technical workers, self-employed, short-term workers, unemployed, retirees, and those not in the labor force.The CPIs are based on prices for food, clothing, shelter, and fuels; transportation fares; service fees (e.g., water and sewer service); and sales taxes. Prices are collected monthly from about 4,000 housing units and approximately 26,000 retail establishments across 87 urban areas. To calculate the index, price changes are averaged with weights representing their importance in the spending of the particular group. The index measures price changes (as a percent change) from a predetermined reference date. In addition to the original unadjusted index distributed, the Bureau of Labor Statistics also releases a seasonally adjusted index. The unadjusted series reflects all factors that may influence a change in prices. However, it can be very useful to look at the seasonally adjusted CPI, which removes the effects of seasonal changes, such as weather, school year, production cycles, and holidays.'
meta = generateFredMeta(headlineCPIYOY_reset, 'headlineCPIYOY', 'US Headline CPI', des)
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
des = 'The spread between 10-Year Treasury Constant Maturity and 2-Year Treasury Constant Maturity'
meta = generateFredMeta(df_reset, series, 'US 10-2 Year Treasury Yield Spread', des)
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
des = 'The breakeven inflation rate represents a measure of expected inflation derived from 10-Year Treasury Constant Maturity Securities and 10-Year Treasury Inflation-Indexed Constant Maturity Securities. The latest value implies what market participants expect inflation to be in the next 10 years, on average.'
meta = generateFredMeta(df_reset, series, 'US 10-Year Breakeven Inflation Rate', des)
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
des = "Gross domestic product (GDP) is the value of the goods and services produced by the nation's economy less the value of the goods and services used up in production. GDP is also equal to the sum of personal consumption expenditures, gross private domestic investment, net exports of goods and services, and government consumption expenditures and gross investment. Real values are inflation-adjusted estimates—that is, estimates that exclude the effects of price changes."
meta = generateFredMeta(df_reset, series, 'US Real GDP Growth (Percent Change from Preceding Period, SAAR)', des)
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
des = "The unemployment rate represents the number of unemployed as a percentage of the labor force. Labor force data are restricted to people 16 years of age and older, who currently reside in 1 of the 50 states or the District of Columbia, who do not reside in institutions (e.g., penal and mental facilities, homes for the aged), and who are not on active duty in the Armed Forces."
meta = generateFredMeta(df_reset, series, 'US Unemployment Rate', des)
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
des = "All Employees: Total Nonfarm, commonly known as Total Nonfarm Payroll, is a measure of the number of U.S. workers in the economy that excludes proprietors, private household employees, unpaid volunteers, farm employees, and the unincorporated self-employed. This measure accounts for approximately 80 percent of the workers who contribute to Gross Domestic Product (GDP). This measure provides useful insights into the current economic situation because it can represent the number of jobs added or lost in an economy. Increases in employment might indicate that businesses are hiring which might also suggest that businesses are growing. Additionally, those who are newly employed have increased their personal incomes, which means (all else constant) their disposable incomes have also increased, thus fostering further economic expansion."
meta = generateFredMeta(df_reset, series, 'US Total Nonfarm', des)
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


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


# %%
series = 'ICSA' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
des = "An initial claim is a claim filed by an unemployed individual after a separation from an employer. The claim requests a determination of basic eligibility for the Unemployment Insurance program."
meta = generateFredMeta(df_reset, series, 'Initial Claims', des)
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
series = 'RRSFS' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
meta = generateFredMeta(df_reset, series, 'Retail Sales')
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)


# %%
series = 'ALTSALES' 
df = fred.get_series(series)
df = df.dropna()
df_reset = df.reset_index()
df_reset = df_reset.dropna()
df_reset.columns = ['Date','Value']
highChartTS = GenerateHighchartVar(df_reset, 'Date','Value')
des = "Light Weight Vehicle Sales: Autos and Light Trucks"
meta = generateFredMeta(df_reset, series, 'Vehicle Sales', des)
generateMetadataFile(meta, series)
generateJSONDataFile(series, highChartTS)

print('Successfully download Fred data')