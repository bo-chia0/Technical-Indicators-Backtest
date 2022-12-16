import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



"""#Data Import and Preprocess"""

wd = 'data/'
ext = 'USDT_1h.csv'
btc_1h = pd.read_csv(wd+'BTC'+ext, header=1)
eth_1h = pd.read_csv(wd+'ETH'+ext, header=1)
bnb_1h = pd.read_csv(wd+'BNB'+ext, header=1)
ada_1h = pd.read_csv(wd+'ADA'+ext, header=1)

def preprocess(df):
	df = df[['date', 'open', 'high', 'low', 'close', 'Volume USDT', 'tradecount']]
	df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume (USDT)', 'Tradecount']
	df = df.sort_values(by='Date')
	df = df.reset_index(drop=True)
	df['Date'] = pd.to_datetime(df['Date'])
	return df

btc_1h = preprocess(btc_1h)
eth_1h = preprocess(eth_1h)
bnb_1h = preprocess(bnb_1h)
ada_1h = preprocess(ada_1h)

"""#High"""

high = {'Date':btc_1h['Date'], 'BTC':btc_1h['High'], 'ETH':eth_1h['High'], 'BNB':bnb_1h['High'], 'ADA':ada_1h['High']}
df_high = pd.DataFrame(data=high)
df_high = df_high.set_index('Date')

"""#Low"""

low = {'Date':btc_1h['Date'], 'BTC':btc_1h['Low'], 'ETH':eth_1h['Low'], 'BNB':bnb_1h['Low'], 'ADA':ada_1h['Low']}
df_low = pd.DataFrame(data=low)
df_low = df_low.set_index('Date')

"""#Close"""

close = {'Date':btc_1h['Date'], 'BTC':btc_1h['Close'], 'ETH':eth_1h['Close'], 'BNB':bnb_1h['Close'], 'ADA':ada_1h['Close']}
df_close = pd.DataFrame(data=close)
df_close = df_close.set_index('Date')

# ploting the closing price
fig, axs = plt.subplots(2, 2, figsize=(16, 8))
axs[0,0].plot(df_close['BTC'])
axs[0,0].set_title('BTC')
axs[0,1].plot(df_close['ETH'])
axs[0,1].set_title('ETH')
axs[1,0].plot(df_close['BNB'])
axs[1,0].set_title('BNB')
axs[1,1].plot(df_close['ADA'])
axs[1,1].set_title('ADA')
plt.suptitle('Prices', fontsize=20)
plt.show()

"""#Volume"""

volume = {'Date':btc_1h['Date'], 'BTC':btc_1h['Volume (USDT)'], 'ETH':eth_1h['Volume (USDT)'], 'BNB':bnb_1h['Volume (USDT)'], 'ADA':ada_1h['Volume (USDT)']}
df_volume = pd.DataFrame(data=volume)
df_volume = df_volume.set_index('Date')

"""#Return"""

# Returns percentage change in the close price and drop the first row with NA's
returns = df_close[['BTC', 'ETH', 'BNB', 'ADA']].pct_change().dropna(axis=0)

#compute the correlations
returns.corr()
#plot the correlations
sns.heatmap(returns.corr(), annot=True, cmap='coolwarm')
plt.title('Return Correlation Matrix', fontsize=20)
plt.show()

#ploting the returns
fig, axs = plt.subplots(2,2,figsize=(24,8))
axs[0,0].plot(returns['BTC'])
axs[0,0].set_title('BTC')
axs[0,0].set_ylim([-0.15, 0.15])
axs[0,1].plot(returns['ETH'])
axs[0,1].set_title('ETH')
axs[0,1].set_ylim([-0.15, 0.15])
axs[1,0].plot(returns['BNB'])
axs[1,0].set_title('BNB')
axs[1,0].set_ylim([-0.15, 0.15])
axs[1,1].plot(returns['ADA'])
axs[1,1].set_title('ADA')
axs[1,1].set_ylim([-0.15, 0.15])
plt.suptitle('Returns', fontsize=20)
plt.show()

#volatility
volatility = returns.std()

#ploting the histogram
fig, axs = plt.subplots(2,2,figsize=(16,8),gridspec_kw ={'hspace': 0.2, 'wspace': 0.1})
axs[0,0].hist(returns['BTC'], bins=50, range=(-0.05, 0.05))
axs[0,0].set_title('BTC')
axs[0,1].hist(returns['ETH'], bins=50, range=(-0.05, 0.05))
axs[0,1].set_title('ETH')
axs[1,0].hist(returns['BNB'], bins=50, range=(-0.05, 0.05))
axs[1,0].set_title('BNB')
axs[1,1].hist(returns['ADA'], bins=50, range=(-0.05, 0.05))
axs[1,1].set_title('ADA')
plt.suptitle('Returns Histogram', fontsize=20)
plt.show()

"""#Cumulative Returns"""

# Cumulative return series
cum_returns = ((1 + returns).cumprod() - 1) *100
cum_returns.plot(figsize=(20,6))
plt.title('Cumulative Returns', fontsize=20)

"""#Moving Average"""

# compute a short-term 20-day moving average
MA20 = df_close.rolling(480).mean()
# compute a Long-term 50-day moving average
MA50 = df_close.rolling(1200).mean()
# compute a Long-term 100-day moving average
MA100 = df_close.rolling(2400).mean()
# ploting the moving average
fig, axs = plt.subplots(2,2,figsize=(24,10),gridspec_kw ={'hspace': 0.2, 'wspace': 0.1})
axs[0,0].plot(df_close['BTC'], label= 'closing')
axs[0,0].plot(MA20['BTC'], label= 'MA20')
axs[0,0].plot(MA50['BTC'], label= 'MA50')
axs[0,0].plot(MA100['BTC'], label= 'MA100')
axs[0,0].set_title('BTC')
axs[0,0].legend()
axs[0,1].plot(df_close['ETH'], label= 'closing')
axs[0,1].plot(MA20['ETH'], label= 'MA20')
axs[0,1].plot(MA50['ETH'], label= 'MA50')
axs[0,1].plot(MA100['ETH'], label= 'MA100')
axs[0,1].set_title('ETH')
axs[0,1].legend()
axs[1,0].plot(df_close['BNB'], label= 'closing')
axs[1,0].plot(MA20['BNB'], label= 'MA20')
axs[1,0].plot(MA50['BNB'], label= 'MA50')
axs[1,0].plot(MA100['BNB'], label= 'MA100')
axs[1,0].set_title('BNB')
axs[1,0].legend()
axs[1,1].plot(df_close['ADA'], label= 'closing')
axs[1,1].plot(MA20['ADA'], label= 'MA20')
axs[1,1].plot(MA50['ADA'], label= 'MA50')
axs[1,1].plot(MA100['ADA'], label= 'MA100')
axs[1,1].set_title('ADA')
axs[1,1].legend()
plt.suptitle('Moving Average (in days)', fontsize=20)
plt.show()

"""#BollingerBands"""

from ta.volatility import BollingerBands

bb_upper, bb_mavg, bb_lower = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
for col in df_close.columns:
	indicator = BollingerBands(df_close[col])
	bb_upper[col] = indicator.bollinger_hband()
	bb_mavg[col] = indicator.bollinger_mavg()
	bb_lower[col] = indicator.bollinger_lband()
plt.figure(figsize=(22,8))
plt.plot(bb_upper['BTC'][1000:2500])
plt.plot(bb_mavg['BTC'][1000:2500])
plt.plot(bb_lower['BTC'][1000:2500])
plt.title('BTC\'s Bollinger Bands', fontsize=20)
plt.show()

"""#RSI"""

from ta.momentum import RSIIndicator

rsi = pd.DataFrame()
for col in df_close.columns:
	indicator = RSIIndicator(df_close[col])
	rsi[col] = indicator.rsi()
plt.figure(figsize=(22,8))
plt.plot(rsi['BTC'][1000:2500])
plt.title('BTC\'s RSI', fontsize=20)
plt.show()

"""#On-balance volume (OBV)"""

from ta.volume import OnBalanceVolumeIndicator

obv = pd.DataFrame()
for col in df_close.columns:
	indicator = OnBalanceVolumeIndicator(df_close[col], df_volume[col])
	obv[col] = indicator.on_balance_volume()
plt.figure(figsize=(22,8))
plt.plot(obv['BTC'][1000:2500])
plt.title('BTC\'s OBV', fontsize=20)
plt.show()

"""#Average True Range"""

from ta.volatility import AverageTrueRange

atr = pd.DataFrame()
for col in df_close.columns:
	indicator = AverageTrueRange(df_high[col], df_low[col], df_close[col])
	atr[col] = indicator.average_true_range()
plt.figure(figsize=(22,8))
plt.plot(atr['BTC'][1000:2500])
plt.title('BTC\'s ATR', fontsize=20)
plt.show()

"""#MACD"""

from ta.trend import MACD

macd = pd.DataFrame()
for col in df_close.columns:
	indicator = MACD(df_close[col])
	macd[col] = indicator.macd_signal()
plt.figure(figsize=(22,8))
plt.plot(macd['BTC'][1000:2500])
plt.title('BTC\'s MACD', fontsize=20)
plt.show()