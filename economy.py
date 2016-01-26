import time
import random
import json
import threading

class Economy:

	def __init__(self):
		with open('economy.json') as f:
			e = json.load(f)
		self.bank = e['accounts']
		self.settings = e['settings']
		self.events = {}

		threading.Timer(self.settings['paydaytimeout'], self.payday).start()
		threading.Timer(300, self.saveBank).start()

	def addAccount(self, accountId):
		if accountId not in self.bank:
			self.bank[accountId] = 0.00

	def checkBalance(self, userid):
		return self.settings['sign'] + str(self.bank[userid])

	def addFunds(self, account, amount):
		self.bank[account] += amount

	def payday(self):
		for account in self.bank:
			self.addFunds(account, self.settings['paydayamount'])

		threading.Timer(self.settings['paydaytimeout'], self.payday).start()

	def commands(self):
		return True

	def saveBank(self):
		self.save()
		threading.Timer(600, self.saveBank).start()

	def save(self):
		data = {'settings': self.settings, 'accounts': self.bank }
		with open('economy.json', 'w') as f:
			json.dump(data, f, indent = 4, sort_keys = True)

	def createEvent(self, minBuyIn, eventId):
		self.events[eventId] = Event(minBuyIn)

	def addBet(self, eventId, account, amount, odds, option):
		self.events[eventId].addBet(account, amount, odds, option)

	def addOption(self, eventId, option):
		self.events[eventId].addOption(option)

	def eventPayout(self, eventId, option):
		for bet in self.events[eventId].bets:
			if bet.option == option:
				self.bank[bet.account] += bet.amount * bet.odds

class Event:

	def __init__(self, minBuyIn):
		self.bets = []
		self.minBuyIn = minBuyIn
		self.options = []

	def addOption(self, option):
		self.options.append(option)

	def addBet(self, account, amount, odds, option):
		if option not in self.options:
			return False

		bet = Bet(account, amount, odds, option)
		self.bets.append(bet)

		return True

class Bet:

	def __init__(self, account, amount, odds, option):
		self.account = account
		self.amount = int(amount)
		self.odds = int(odds)
		self.option = option