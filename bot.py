import discord
import time
import random
import json
import threading

f = open("settings.txt", "r")
loginInfo = f.read().split(":")
f.close()

admins = []
status = { 
	"debug": False,
	"trivia": False,
	"trivia_channel": ""
}

client = discord.Client()
client.login(loginInfo[0], loginInfo[1])

if not client.is_logged_in:
	print("SYS: Failed to login")
	exit(1)

def handleCommand(args, msg):
	global status
	global admins

	command = args[0].strip("!").lower()

	if command == "help":
		print("SYS: Replying with help")
		client.send_message(msg.channel, "I am a bot. I insult Hex.")
		client.send_message(msg.channel, "__**Commands**__")
		client.send_message(msg.channel, "**!help** - List of commands")
		client.send_message(msg.channel, "**!exit** *admin only* - close the bot")
		client.send_message(msg.channel, "**!admins** - List of bot admins [WIP]")
		client.send_message(msg.channel, "**!setadmin** *admin only* - set mentioned users as admins on the bot")
		client.send_message(msg.channel, "**!removeadmin** *admin only* - removes mentioned users from being bot admins")
		client.send_message(msg.channel, "**!addinsult** - adds an insult to the list of available insults")
		client.send_message(msg.channel, "**!insult** - insults the first mentioned user")
	elif command == "exit":
		if checkPrivilege(msg.author.id):
			print("SYS: Closing...")
			exit(1)
	elif command == "setadmin":
		if checkPrivilege(msg.author.id):
			for user in msg.mentions:
				if user.id not in admins:
					print("SYS: Adding {} as admin".format(user.name))
					admins.append(user.id)

			f = open("admins.txt", "w")
			f.write(",".join(admins))
			f.close()
	elif command == "removeadmin":
		if checkPrivilege(msg.author.id):
			for user in msg.mentions:
				print("SYS: Removing {} as admin".format(user.name))
				admins.remove(user.id)

			f = open("admins.txt", "w")
			f.write(",".join(admins))
			f.close()
	elif command == "admins":
		print("SYS: Listing admins")
		client.send_message(msg.channel, "Current bot admins are:")
		for admin in admins:
			client.send_message(msg.channel, "- {}".format(admin))
	elif command == "insult":
		insults = open("insults.txt", "r").read().splitlines()
		insult = random.choice(insults)
		tts = False

		if len(args) > 2:
			if args[2] == "tts":
				tts = True

		client.send_message(msg.channel, insult.replace("$user", args[1]), True, tts)
	elif command == "addinsult":
		insult = args
		insult.pop(0)
		f = open("insults.txt", "a")
		f.write(" ".join(insult) + "\n")
		f.close()
		client.send_message(msg.channel, "Added")
	elif command == "trivia":
		if args[1] == "on":
			status["trivia"] = True
			status["trivia_channel"] = msg.channel.id
	elif command == "status":
		if checkPrivilege(msg.author.id):
			client.send_message(msg.channel, "```" + json.dumps(status) + "```")
	elif command == "flip":
		client.send_message(msg.channel, random.choice(["HEADS", "TAILS"]))


def checkPrivilege(id):
	if id in admins:
		return True
	else:
		return False

@client.event
def on_message(msg):
	if msg.author.id == client.connection.user.id:
		return

	print("MSG: [{}:{}] -> {}:{} : {}".format(str(msg.author), msg.author.id, msg.channel.name, msg.channel.id, msg.content.encode("utf-8")))

	if msg.content.startswith("!"):
		args = msg.content.split(" ")
		handleCommand(args, msg)

@client.event
def on_ready():
	global admins

	print("SYS: Loading admins...")

	f = open("admins.txt", "r")
	admins = f.read().split(",")
	f.close()

	print("SYS: Bot is running as {}".format(client.user.name))

print("SYS: Starting bot...")
client.run()