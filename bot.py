import discord
import asyncio
import random
import json

with open('settings.json') as f:
	settings = json.load(f)

with open('insults.json') as f:
	insults = json.load(f)

client = discord.Client()

async def HandleCommand(msg, client):
	args = msg.content.split(' ')
	command = args[0].strip(settings['commandCharacter']).lower()
	args.pop(0)

	if command == 'help':
		await client.send_message(msg.channel, 'I am a bot. I insult Hex.')
		await client.send_message(msg.channel, '__**Commands**__')
		await client.send_message(msg.channel, '**!help** - list of commands')
		await client.send_message(msg.channel, '**!exit** *admin only* - close the bot')
		await client.send_message(msg.channel, '**!admins** - List of admins [Work in Progress]')
		await client.send_message(msg.channel, '**!insult** - Insults the first mentioned user')
		await client.send_message(msg.channel, '**!addinsult** - Add an insult to the bots insult list. Denote the insultee with $user (tts currently disabled)')
	elif command == 'insult':
		await client.send_message(msg.channel, (random.choice(insults)).replace('$user', args[1]))
	elif command == 'addinsult':
		insults.append(' '.join(args))
		saveFile('insults.json', insults)
		await client.send_message(msg.channel, 'Added')
	elif command == 'admins':
		await client.send_message(msg.channel, 'Bot Admins:')
		for admin in settings['admins']:
			await client.send_message(msg.channel, admin)

		await client.send_message(msg.channel, 'Server Admins:')
		for member in msg.server.members:
			for role in member.roles:
				if role.name == settings['adminRole']:
					await client.send_message(msg.channel, member.name)
	elif command == 'flip':
		await client.send_message(msg.channel, random.choice(["HEADS", "TAILS"]))
	elif command == 'exit':
		if checkPrivilege(msg.author.id):
			exit(1)

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

@client.async_event
async def on_ready():
	print('SYS: Bot is running as {}'.format(client.user.name))

def main():
	client.run(settings['login']['email'], settings['login']['password'])

if __name__ == '__main__':
	main()