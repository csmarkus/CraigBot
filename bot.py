import discord
import asyncio
import random
import json
from economy import Economy

with open('settings.json') as f:
	settings = json.load(f)

with open('insults.json') as f:
	insults = json.load(f)

client = discord.Client()
economy = Economy()

async def HandleCommand(msg, client):
	args = msg.content.split(' ')
	command = args[0].strip(settings['commandCharacter']).lower()
	args.pop(0)

	if command == 'help':
		await client.send_message(msg.channel, 'I am a bot. I insult Hex.')
		await client.send_message(msg.channel, '__**Commands**__')
		await client.send_message(msg.channel, '**!help** - list of commands')
		await client.send_message(msg.channel, '**!insult** - Insults the first mentioned user')
		await client.send_message(msg.channel, '**!insulttts** - Insults the first mentioned user and reads it out')
		await client.send_message(msg.channel, '**!addinsult** - Add an insult to the bots insult list. Denote the insultee with $user')
		await client.send_message(msg.channel, '**!balance** - check your economy balance')
	elif command == 'insult':
		await client.send_message(msg.channel, (random.choice(insults)).replace('$user', args[0]))
	elif command == 'insulttts':
		await client.send_message(msg.channel, (random.choice(insults)).replace('$user', args[0]), tts=True)
	elif command == 'addinsult':
		insults.append(' '.join(args))
		saveFile('insults.json', insults)
		await client.send_message(msg.channel, 'Added')
	elif command == 'flip':
		await client.send_message(msg.channel, random.choice(["HEADS", "TAILS"]))
	elif command == 'slap':
		await client.send_message(msg.channel, "*slaps {} with a trout*".format(args[0]))
	elif command == 'exit':
		if checkPrivilege(msg.author.id):
			exit(1)
	elif command == 'balance':
		await client.send_message(msg.channel, " {}'s Balance: {}".format(msg.author.mention, economy.checkBalance(msg.author.id)))
	elif command == 'name':
		if checkPrivilege(msg.author.id):
			await client.edit_profile(settings['login']['password'], username=args[0])
	elif command == 'save':
		economy.save()
	elif command == 'createevent':
		economy.createEvent(args[0], args[1])
	elif command == 'addoption':
		economy.addOption(args[0], args[1])
	elif command == 'bet':
		economy.addBet(args[0], msg.author.id, args[1], args[2], args[3])
	elif command == 'payout':
		economy.eventPayout(args[0], args[1])

def saveFile(file, data):
	with open(file, 'w') as f:
		json.dump(data, f, indent = 4, sort_keys = True)

def checkPrivilege(id):
	if id in settings['admins']:
		return True
	else:
		return False

@client.async_event
async def on_message(msg):
	if msg.content.startswith(settings['commandCharacter']):
		await HandleCommand(msg, client)
	else:
		economy.addFunds(msg.author.id, 0.25)

@client.async_event
async def on_ready():
	print('SYS: Bot is running as {}'.format(client.user.name))

	server = client.get_server('66142305177841664')

	for member in server.members:
		economy.addAccount(member.id)

def main():
	client.run(settings['login']['email'], settings['login']['password'])

if __name__ == '__main__':
	main()