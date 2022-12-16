#	Import packages
from statistics import stdev
import pandas as pd
import numpy as np

class Account:
	def __init__(self, balance:int=100000) -> None:
		self.init_balance = balance	
		self.balance = balance
		self.asset_amount = 0
		self.order_history = pd.DataFrame(columns=['Date', 'Buy/Sell', 'Amount', 'Price', 'Profit'])
		self.ret_hist = []
		self.hold = 0
		self.buy_price = 0

	def set_balance(self, balance:int) -> None:
		self.balance = balance

	def set_asset_value(self, asset_value:int) -> None:
		self.asset_value = asset_value

	def buy(self, date, price):
		self.hold = 1	#	holding crypto 
		self.buy_price = price
		self.asset_amount = self.balance/price
		self.balance = 0
		self.order_history = self.order_history.append({'Date':date, 'Buy/Sell':'buy', 
			'Amount':round(self.asset_amount, 2), 'Price':price, 'Profit':0}, ignore_index = True)

	def sell(self, date, price):
		self.hold = 0	#	not holding crypto 
		self.balance = self.asset_amount*price
		profit = self.asset_amount*(price-self.buy_price)
		self.ret_hist.append((price-self.buy_price)/self.buy_price)
		self.order_history = self.order_history.append({'Date':date, 'Buy/Sell':'sell', 
			'Amount':round(self.asset_amount, 2), 'Price':price, 'Profit':profit}, ignore_index = True)
		self.asset_amount = 0

	def win_rate(self):
		order_history = self.order_history
		win = len(order_history[order_history['Profit']>0])		#	trades that made profit
		lose = len(order_history[order_history['Profit']<0])	#	trades that lost
		win_rate = round(win/(win+lose),3)
		print('Win rate is {}%'.format(win_rate*100))
		return win_rate
  
	def total_profit(self):
		total_profit = round(sum(self.order_history['Profit']), 2)	#	total profit made
		print('Profit is {}'.format(total_profit))
		return total_profit

	def total_return(self):
		total_return = round((self.balance-self.init_balance)/self.init_balance, 3)	#	final balance / initial balance
		print('Total Return is {}%'.format(total_return*100))
		return total_return
	
	def volatility(self):
		volatility = round(stdev(self.ret_hist), 4)	#	return's standard deviation is its risk
		print('Volatility is {}%'.format(volatility*100))
		return volatility

	def mean_volatility_ratio(self):
		mean_volatility = round(np.mean(self.ret_hist)/stdev(self.ret_hist), 3)	#	mean/volatility
		print('Mean Volatility Ratio is {}'.format(mean_volatility))
		return mean_volatility
