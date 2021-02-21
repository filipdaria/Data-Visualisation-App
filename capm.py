import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
current_stock='AAPL MSFT IHG ^GSPC'
split_stock = current_stock.split(' ')
size=len(split_stock)
# print(split_stock)
given_period="1mo"
stock_data = yf.download(current_stock, period=given_period)
df= pd.DataFrame(data=stock_data.iloc[:,size:2*size])


def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            df_daily_return[i][j] = ((df[i][j]- df[i][j-1])/df[i][j-1]) * 100
        df_daily_return[i][0] = 0
    return df_daily_return
stocks_return = daily_return(df)
# print(stocks_return)
beta = {}
alpha = {}
for i in stocks_return.iloc[:,:-1]:
    b, a = np.polyfit(stocks_return.iloc[:,-1], stocks_return[i], 1)
    beta[i] = b    
    alpha[i] = a  
# print(beta)
# print(alpha)
# keys = list(beta.keys())
ER = {}
rf = 0 
keys = list(beta.keys())
rm = stocks_return.iloc[:,-1].mean() * 252 

for i in keys:
    ER[i] = rf + (beta[i] * (rm-rf))
print(ER)
portfolio_weights = 1/(size-1) * np.ones(size-1) 
ER_portfolio = sum(list(ER.values()) * portfolio_weights)
print(ER_portfolio)
