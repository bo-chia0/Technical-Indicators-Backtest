###-----------------------------------------------------------------------------------------###
"""Import Packages"""
###-----------------------------------------------------------------------------------------###
import pandas as pd
import numpy as np
from Account import Account
import itertools

###-----------------------------------------------------------------------------------------###
"""Data Import and Preprocess"""
###-----------------------------------------------------------------------------------------###

#	Read OHLC files kept in folder 'data'
wd = '../data/'
ext = 'USDT_1h.csv'
btc_1h = pd.read_csv(wd+'BTC'+ext, header=1)
eth_1h = pd.read_csv(wd+'ETH'+ext, header=1)
bnb_1h = pd.read_csv(wd+'BNB'+ext, header=1)
ada_1h = pd.read_csv(wd+'ADA'+ext, header=1)

def preprocess(df):
	df = df[['date', 'open', 'high', 'low', 'close', 'Volume USDT', 'tradecount']]		#	Only keep columns needed	
	df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume (USDT)', 'Tradecount']#	Change the column names
	df = df.sort_values(by='Date')				#	Sort by 'Date'
	df = df.reset_index(drop=True)				#	Reset index
	df['Date'] = pd.to_datetime(df['Date'])		#	Convert 'Date' to class "Timestamp"
	return df

#	arrange every crypto's data
btc_1h = preprocess(btc_1h)
eth_1h = preprocess(eth_1h)
bnb_1h = preprocess(bnb_1h)
ada_1h = preprocess(ada_1h)


###-----------------------------------------------------------------------------------------###
"""基本資料"""
###-----------------------------------------------------------------------------------------###


"""High"""
high = {'Date':btc_1h['Date'], 'BTC':btc_1h['High'], 'ETH':eth_1h['High'], 'BNB':bnb_1h['High'], 'ADA':ada_1h['High']}
df_high = pd.DataFrame(data=high)
df_high = df_high.set_index('Date')

"""Low"""
low = {'Date':btc_1h['Date'], 'BTC':btc_1h['Low'], 'ETH':eth_1h['Low'], 'BNB':bnb_1h['Low'], 'ADA':ada_1h['Low']}
df_low = pd.DataFrame(data=low)
df_low = df_low.set_index('Date')

"""Close"""
close = {'Date':btc_1h['Date'], 'BTC':btc_1h['Close'], 'ETH':eth_1h['Close'], 'BNB':bnb_1h['Close'], 'ADA':ada_1h['Close']}
df_close = pd.DataFrame(data=close)
df_close = df_close.set_index('Date')

"""Volume"""
volume = {'Date':btc_1h['Date'], 'BTC':btc_1h['Volume (USDT)'], 'ETH':eth_1h['Volume (USDT)'], 'BNB':bnb_1h['Volume (USDT)'], 'ADA':ada_1h['Volume (USDT)']}
df_volume = pd.DataFrame(data=volume)
df_volume = df_volume.set_index('Date')

"""Return"""
# Returns percentage change in the close price and drop the first row with NA's
returns = df_close[['BTC', 'ETH', 'BNB', 'ADA']].pct_change().dropna(axis=0)

"""Cumulative Returns"""
# Cumulative return series
cum_returns = ((1 + returns).cumprod() - 1) *100


###-----------------------------------------------------------------------------------------###
"""技術指標"""	#	All the technical analysis are calculated using ta library and saved in dataframe.
###-----------------------------------------------------------------------------------------###


"""Moving Average"""

# compute a short-term 1-day moving average
ma1 = df_close.rolling(24).mean()
# compute a Long-term 5-day moving average
ma5 = df_close.rolling(120).mean()
# compute a Long-term 10-day moving average
ma10 = df_close.rolling(240).mean()
# compute a short-term 20-day moving average
ma20 = df_close.rolling(480).mean()
# compute a Long-term 50-day moving average
ma50 = df_close.rolling(1200).mean()
# compute a Long-term 100-day moving average
ma100 = df_close.rolling(2400).mean()

"""BollingerBands"""

from ta.volatility import BollingerBands

bb_upper, bb_mavg, bb_lower = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
for col in df_close.columns:
	indicator = BollingerBands(df_close[col])
	bb_upper[col] = indicator.bollinger_hband()
	bb_mavg[col] = indicator.bollinger_mavg()
	bb_lower[col] = indicator.bollinger_lband()

"""RSI"""

from ta.momentum import RSIIndicator

rsi = pd.DataFrame()
for col in df_close.columns:
	indicator = RSIIndicator(df_close[col])
	rsi[col] = indicator.rsi()

"""On-balance volume (OBV)"""

from ta.volume import OnBalanceVolumeIndicator

obv = pd.DataFrame()
for col in df_close.columns:
	indicator = OnBalanceVolumeIndicator(df_close[col], df_volume[col])
	obv[col] = indicator.on_balance_volume()

"""Average True Range"""

from ta.volatility import AverageTrueRange

atr = pd.DataFrame()
for col in df_close.columns:
	indicator = AverageTrueRange(df_high[col], df_low[col], df_close[col])
	atr[col] = indicator.average_true_range()

"""MACD"""

from ta.trend import MACD

macd = pd.DataFrame()
for col in df_close.columns:
	indicator = MACD(df_close[col])
	macd[col] = indicator.macd_signal()


###-----------------------------------------------------------------------------------------###
"""實際交易"""
###-----------------------------------------------------------------------------------------###

cryptos = ['BTC', 'ETH', 'BNB', 'ADA']	# 4 different cryptos
date = df_close.index



"""Strategy -- Buy and hold"""
win_rate_list = []			#	Record win rate
return_list = []			#	Record return

for cryp in cryptos:

	print('{} with strategy of buy and hold.'.format(cryp))	#	Make the result easy to view
	acc = Account()
	
	acc.buy(date[0], df_close[cryp][0])
	acc.sell(df_close.index[len(df_close)-1], df_close[cryp][len(df_close)-1])

	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view

df_win_rate = pd.DataFrame(win_rate_list, index=cryptos, columns=['Buy&Hold'])		#	Create DataFrame to record win rate 
df_return = pd.DataFrame(return_list, index=cryptos, columns=['Buy&Hold'])			#	Create DataFrame to record return






"""Strategy -- MA"""

ma = {'MA1':ma1, 'MA5':ma5, 'MA10':ma10, 'MA20':ma20, 'MA50':ma50, 'MA100':ma100}	#	將不同時間段之MA存入Dictionary，方便在迴圈操作

win_rate_all = []	#	紀錄不同搭配之勝率
return_all = []		#	紀錄不同搭配之報酬率
vol_all = []		#	紀錄不同搭配之風險
mean_vol_all = []	#	紀錄不同搭配之Mean-Volatility ratio
colnames=['1&5', '1&10', '1&20', '1&50', '1&100',			
          '5&10', '5&20', '5&50', '5&100',
          '10&20', '10&50', '10&100', '20&50','20&100', '50&100']	#	勝率、報酬率DataFrame之欄位名稱

                                                                        
for cryp in cryptos:		#	Run 4 different cryptos
	win_rate_list = []	#	Win rate for the current crypto 
	return_list = []	#	Return for the current crypto 
	vol_list = []		#	Volatility for the current crypto 
	mean_vol_list = []	#	Mean-Volatility ratio for the current crypto 
	for a, b in itertools.combinations(ma, 2):	#	For all the ma combinations (ex. 5&20, 10&50)
		acc = Account()	#	Create an account
		print('{} with strategy of {} and {} golden crosses.'.format(cryp, a, b))	#	Make the result easy to view

		a = ma[a]	#	a is DataFrame for the shorter-day MA
		b = ma[b]	#	b is DataFrame for the longer-day MA
		for i in range(1, len(df_close[cryp])):
			if (a[cryp][i] > b[cryp][i]) and (a[cryp][i-1] < b[cryp][i-1]):		#	When shorter-day MA breakthrough longer-day MA
				if acc.hold == 0:										#	and holds no asset 
					acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	buy
			elif (a[cryp][i] < b[cryp][i]) and (a[cryp][i-1] > b[cryp][i-1]):	#	When shorter-day MA collapse hrough longer-day MA
				if acc.hold == 1:										#	and holds asset 
					acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell
		if acc.hold == 1:												#	if account still holds asset at the end
			acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell
		
		win_rate_list.append(acc.win_rate())				#	Record win rate for current ma combination
		return_list.append(acc.total_return())				#	Record return for current ma combination
		vol_list.append(acc.volatility())					#	Record volatility for current ma combination
		mean_vol_list.append(acc.mean_volatility_ratio())	#	Record mean-volatility ratio for current ma combination
		
		acc.total_profit()			#	Print results
		print(acc.order_history)		#	Print results
		print('\n---------------------------------------------------------------\n')	#	Make the result easy to view
	
	win_rate_all.append(win_rate_list)	#	Record win rate for the current crypto 
	return_all.append(return_list)		#	Record return for the current crypto 
	vol_all.append(vol_list)			#	Record win rate for the current crypto 
	mean_vol_all.append(mean_vol_list)	#	Record return for the current crypto 

df_win_rate_ma = pd.DataFrame(win_rate_all, columns=colnames, index=cryptos)	#	Dataframe record win rate for every	combinations
df_return_ma = pd.DataFrame(return_all, columns=colnames, index=cryptos)		#	Dataframe record return for every combinations
df_vol_ma = pd.DataFrame(vol_all, columns=colnames, index=cryptos)				#	Dataframe record volatility for every	combinations
df_mean_vol_ma = pd.DataFrame(mean_vol_all, columns=colnames, index=cryptos)	#	Dataframe record mean-volatility ratio for every combinations

df_win_rate_ma.to_csv('../Results/MA_WinRate.csv')					#	Export as .csv
df_return_ma.to_csv('../Results/MA_Return.csv')					#	Export as .csv
df_vol_ma.to_csv('../Results/MA_Volatility.csv')					#	Export as .csv
df_mean_vol_ma.to_csv('../Results/MA_Mean_Volatility_Ratio.csv')	#	Export as .csv





"""Strategy -- MACD"""

win_rate_list = []			#	Record win rate
return_list = []			#	Record return
volatility_list = []		#	Record volatility
mean_volatility_list = []	#	Record mean volatility ratio

for cryp in cryptos:	#	For 4 cryptos,

	print('{} with strategy of MACD golden crosses.'.format(cryp))	#	Make the result easy to view
	acc = Account()		#	Create an account

	for i in range(1, len(df_close[cryp])):
		if (macd[cryp][i] > 0) and (macd[cryp][i-1] <= 0):					#	When MACD breakthrough 0
			if acc.hold == 0:												#	and holds no asset 
				acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	buy
		elif (macd[cryp][i] < 0) and (macd[cryp][i-1] >= 0):				#	When MACD collapse through 0
			if acc.hold == 1:												#	and holds asset 
				acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell
	if acc.hold == 1:														#	if account still holds asset at the end
		acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])			#	sell
	
	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 
	volatility_list.append(acc.volatility())					#	Record win rate 
	mean_volatility_list.append(acc.mean_volatility_ratio())	#	Record return 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view

df_win_rate['MACD'] = win_rate_list		#	Record Strategy MACD's win rate
df_return['MACD'] = return_list			#	Record Strategy MACD's return
df_volatility = pd.DataFrame(volatility_list, index=cryptos, columns=['MACD'])			#	Create DataFrame to record volatility
df_mean_volatility = pd.DataFrame(mean_volatility_list, index=cryptos, columns=['MACD'])#	Create DataFrame to record mean volatility ratio





"""Strategy -- Bollinger Bands"""
win_rate_list = []			#	Record win rate
return_list = []			#	Record return
volatility_list = []		#	Record volatility
mean_volatility_list = []	#	Record mean volatility ratio

for cryp in cryptos:	#	For 4 cryptos,

	print('{} with strategy of Bollinger Bands.'.format(cryp))	#	Make the result easy to view
	acc = Account()		#	Create an account

	for i in range(1, len(df_close[cryp])):
		if (df_close[cryp][i] < bb_lower[cryp][i]) and (df_close[cryp][i-1] >= bb_lower[cryp][i-1]):	#	When price breakthrough Bollinger Band
			if acc.hold == 0:																			#	and holds no asset 
				acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])								#	buy
		elif (df_close[cryp][i] > bb_upper[cryp][i]) and (df_close[cryp][i-1] <= bb_upper[cryp][i-1]):	#	When price collapse through Bollinger Band
			if acc.hold == 1:																			#	and holds asset 
				acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])								#	sell
	if acc.hold == 1:																					#	if account still holds asset at the end
		acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])										#	sell

	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 
	volatility_list.append(acc.volatility())					#	Record volatility
	mean_volatility_list.append(acc.mean_volatility_ratio())	#	Record mean volatility ratio 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view

df_win_rate['Bollinger Bands'] = win_rate_list		#	Record Strategy Bollinger Bands's win rate
df_return['Bollinger Bands'] = return_list			#	Record Strategy Bollinger Bands's return
df_volatility['Bollinger Bands'] = volatility_list	#	Record Strategy Bollinger Bands's volatility
df_mean_volatility['Bollinger Bands'] = mean_volatility_list	#	Record Strategy Bollinger Bands's mean volatility ratio




"""Strategy -- RSI"""
win_rate_list = []			#	Record win rate
return_list = []			#	Record return
volatility_list = []		#	Record volatility
mean_volatility_list = []	#	Record mean volatility ratio

for cryp in cryptos:	#	For 4 cryptos,

	print('{} with strategy of RSI.'.format(cryp))	#	Make the result easy to view
	acc = Account()		#	Create an account

	for i in range(1, len(df_close[cryp])):
		if (rsi[cryp][i] < 20) and (rsi[cryp][i-1] >= 20):					#	When RSI collapse through 20 (超賣)
			if acc.hold == 0:												#	and holds no asset 
				acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	buy
		elif (rsi[cryp][i] > 80) and (rsi[cryp][i-1] <= 80):				#	When RSI breakthrough 80 (超買)
			if acc.hold == 1:												#	and holds asset 
				acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell
	if acc.hold == 1:												#	if account still holds asset at the end
		acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell

	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 
	volatility_list.append(acc.volatility())					#	Record volatility
	mean_volatility_list.append(acc.mean_volatility_ratio())	#	Record mean volatility ratio 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view


df_win_rate['RSI'] = win_rate_list					#	Record Strategy RSI's win rate
df_return['RSI'] = return_list						#	Record Strategy RSI's return
df_volatility['RSI'] = volatility_list				#	Record Strategy RSI's volatility
df_mean_volatility['RSI'] = mean_volatility_list	#	Record Strategy RSI's mean volatility ratio




###-----------------------------------------------------------------------------------------###
###-----------------------------------------------------------------------------------------###
"""實際交易--進階策略"""
###-----------------------------------------------------------------------------------------###
###-----------------------------------------------------------------------------------------###
"""Strategy -- MACD with ATR"""

win_rate_list = []			#	Record win rate
return_list = []			#	Record return
volatility_list = []		#	Record volatility
mean_volatility_list = []	#	Record mean volatility ratio

for cryp in cryptos:	#	For 4 cryptos,

	print('{} with strategy of MACD and ATR.'.format(cryp))	#	Make the result easy to view
	acc = Account()		#	Create an account

	atr_mean = np.mean(atr[cryp])

	for i in range(1, len(df_close[cryp])):
		if (macd[cryp][i] > 0) and (macd[cryp][i-1] <= 0) and (atr[cryp][i] >= atr_mean):	#	When MACD breakthrough 0 and ATR is high
			if acc.hold == 0:																#	and holds no asset 
				acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])					#	buy
		elif (macd[cryp][i] < 0) and (macd[cryp][i-1] >= 0) and (atr[cryp][i] >= atr_mean):	#	When MACD collapse through 0 and ATR is high
			if acc.hold == 1:																#	and holds asset 
				acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])					#	sell
	if acc.hold == 1:																		#	if account still holds asset at the end
		acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])							#	sell
	
	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 
	volatility_list.append(acc.volatility())					#	Record win rate 
	mean_volatility_list.append(acc.mean_volatility_ratio())	#	Record return 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view

df_win_rate['MACD+ATR'] = win_rate_list					#	Record Strategy MACD+ATR's win rate
df_return['MACD+ATR'] = return_list						#	Record Strategy MACD+ATR's return
df_volatility['MACD+ATR'] = volatility_list				#	Record Strategy MACD+ATR's volatility
df_mean_volatility['MACD+ATR'] = mean_volatility_list	#	Record Strategy MACD+ATR's mean volatility ratio


"""Strategy -- MA1 with OBV"""

win_rate_list = []			#	Record win rate
return_list = []			#	Record return
volatility_list = []		#	Record volatility
mean_volatility_list = []	#	Record mean volatility ratio

for cryp in cryptos:	#	For 4 cryptos,

	print('{} with strategy of MA1 with OBV.'.format(cryp))	#	Make the result easy to view
	acc = Account()		#	Create an account

	for i in range(1, len(df_close[cryp])):
		if (obv[cryp][i] > ma1[cryp][i]) and (obv[cryp][i-1] <= ma1[cryp][i-1]):					#	When MACD breakthrough 0
			if acc.hold == 0:												#	and holds no asset 
				acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	buy
		elif (obv[cryp][i] < ma1[cryp][i]) and (obv[cryp][i-1] >= ma1[cryp][i-1]):				#	When MACD collapse through 0
			if acc.hold == 1:												#	and holds asset 
				acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell
	if acc.hold == 1:														#	if account still holds asset at the end
		acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])			#	sell
	
	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 
	volatility_list.append(acc.volatility())					#	Record win rate 
	mean_volatility_list.append(acc.mean_volatility_ratio())	#	Record return 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view

df_win_rate['MA1+OBV'] = win_rate_list		#	Record Strategy MA1+OBV's win rate
df_return['MA1+OBV'] = return_list			#	Record Strategy MA1+OBV's return
df_volatility['MA1+OBV'] = volatility_list				#	Record Strategy MA1+OBV's volatility
df_mean_volatility['MA1+OBV'] = mean_volatility_list	#	Record Strategy MA1+OBV's mean volatility ratio



"""Strategy -- MA5 with OBV"""

win_rate_list = []			#	Record win rate
return_list = []			#	Record return
volatility_list = []		#	Record volatility
mean_volatility_list = []	#	Record mean volatility ratio

for cryp in cryptos:	#	For 4 cryptos,

	print('{} with strategy of MA5 with OBV.'.format(cryp))	#	Make the result easy to view
	acc = Account()		#	Create an account

	for i in range(1, len(df_close[cryp])):
		if (obv[cryp][i] > ma5[cryp][i]) and (obv[cryp][i-1] <= ma5[cryp][i-1]):					#	When MACD breakthrough 0
			if acc.hold == 0:												#	and holds no asset 
				acc.buy(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	buy
		elif (obv[cryp][i] < ma5[cryp][i]) and (obv[cryp][i-1] >= ma5[cryp][i-1]):				#	When MACD collapse through 0
			if acc.hold == 1:												#	and holds asset 
				acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])	#	sell
	if acc.hold == 1:														#	if account still holds asset at the end
		acc.sell(df_close[cryp].index[i], df_close[cryp].iloc[i, ])			#	sell
	
	win_rate_list.append(acc.win_rate())						#	Record win rate 
	return_list.append(acc.total_return())						#	Record return 
	volatility_list.append(acc.volatility())					#	Record win rate 
	mean_volatility_list.append(acc.mean_volatility_ratio())	#	Record return 

	acc.total_profit()			#	Print results
	print(acc.order_history)	#	Print results
	print('\n---------------------------------------------------------------\n')	#	Make the result easy to view

df_win_rate['MA5+OBV'] = win_rate_list		#	Record Strategy MA5+OBV's win rate
df_return['MA5+OBV'] = return_list			#	Record Strategy MA5+OBV's return
df_volatility['MA5+OBV'] = volatility_list				#	Record Strategy MA5+OBV's volatility
df_mean_volatility['MA5+OBV'] = mean_volatility_list	#	Record Strategy MA5+OBV's mean volatility ratio


###-----------------------------------------------------------------------------------------###
###-----------------------------------------------------------------------------------------###
"""輸出結果"""
###-----------------------------------------------------------------------------------------###
###-----------------------------------------------------------------------------------------###
df_win_rate.to_csv('../Results/ALL_WinRate.csv')		#	Export as .csv
df_return.to_csv('../Results/ALL_Return.csv')			#	Export as .csv
df_volatility.to_csv('../Results/ALL_Volatility.csv')		#	Export as .csv
df_mean_volatility.to_csv('../Results/ALL_Mean_Volatility.csv')	#	Export as .csv