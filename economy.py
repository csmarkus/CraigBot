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

		threading.Timer(self.settings['paydaytimeout'], self.payday).start()
		threading.Timer(600, self.saveBank).start()

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
		data = {'settings': self.settings, 'accounts': self.bank }
		with open('economy.json', 'w') as f:
			json.dump(data, f, indent = 4, sort_keys = True)

		threading.Timer(600, self.saveBank).start()