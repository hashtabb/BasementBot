import discord
import asyncio

'''
	TO-DO's (for others trying to use):
		1. Locate client_id of your server (This will be found on discord site, under bots)
		2. Find token for bot (same location as above)
		3. Fill in the variables below with values
'''
clientId = 0
botToken = "FILL IN"
mainChannelID = 0 #Used for sending messages / parsing messages in a certain channel

def game_info():
	ongoinggame = open('bestof.txt', 'r')
	ongoinggame.readline()
	players = ongoinggame.readline().strip().split()
	score = ongoinggame.readline().strip().split()
	ongoinggame.close()
	return "score: {} - {}, {} - {}".format(players[0],score[0], players[2], score[1])

def rps(msg1, msg2, name1, name2):
	
	msg1 = msg1.lower()
	msg2 = msg2.lower()
	if msg1.lower() == msg2.lower():
		return "It's a tie! Use '!rps' to play again"
	elif (msg1 == "rock" and msg2 == "scissors") or (msg1 == "scissors" and msg2 == "paper") or (msg1 == "paper" and msg2 == "rock"):
		return "{} has won the rps!".format(name1)
	elif (msg2 == "rock" and msg1 == "scissors") or (msg2 == "scissors" and msg1 == "paper") or (msg2 == "paper" and msg1 == "rock"):
		return "{} has won the rps!".format(name2)
	else:
		return "Something went wrong! Check your spelling"

client = discord.Client()



class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
		# NEED TO FILL IN WITH CHANNEL ID
        channel = self.get_channel(clientID) # channel ID goes in here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(10) # task runs every 60 seconds

'''
	MESSAGE JOIN FUNCTION:
'''
@client.event
async def on_member_join(member):
	channel = client.get_channel(mainChannelID)
	await channel.send(f"{member} joined the server. Because we didn't have enough basement dwellers already :/")

'''
	NICKNAME CHANGED FUNCTION:
'''
@client.event
async def on_member_update(before, after):
	if before.nick != after.nick:
		channel = client.get_channel(mainChannelID)
		await channel.send(f"tbh i liked the old {before.nick}, y'know, before they switched their name and all that")

'''
	BOT @'ed FUNCTION:
		- is called after anyone sends a message with @BasementBot (or whatever you called your bot)
'''
@client.event
async def mentioned_in(message):
	await message.channel.send("solve your own issues")

'''
	MESSAGE PARSER FUNCTION:
		- The two first if statements are important, most else can be deleted 
		- This is the place to be creative :)
'''
@client.event
async def on_message(message):

	'''
		THIS IF STATEMENT IS IMPORTANT, DO NOT REMOVE
			- Prevents the bot from parsing the messages it just sent (prevents infinite message loops)
	'''
	if (message.author.id == client.user.id):
		return

	'''
		TERMINATE BOT
			- Customize the string below, as a phrase to automatically shut down the bot
	'''
	elif "get outta here" in message.content.lower():
		await client.close()


	if "hi there" in message.content.lower():
		await message.channel.send("HI!")

	#SpongeBob Meme-ifier
	elif "stupid" in message.content.lower() and message.author != client.user:
		newstring = ""
		countvar = 0
		for char in message.content:
			if countvar%2 == 0:
				newstring += char.upper()
				countvar += 1
			else:
				newstring += char.lower()
				countvar += 1
		await message.channel.send(newstring + " see, thats what you sound like right now. That's you.")


	#Bot Tagged
	elif "604076680209891329" in message.content.lower():
		await message.channel.send("please stop being so needy for once and learn to do things yourself")

	elif "snake" in message.content.lower() and message.author != client.user:
		await message.channel.send(":snake:")





	elif "!timefortheboys" in message.content.lower():
		await message.channel.send("When is it time for the boys?")

		try:
			global msg
			global boystime
			boystime = "true"
			msg = await client.wait_for("message", timeout = 10)

		except asyncio.TimeoutError:
			await message.channel.send("I guess there's no time for the boys anymore :(")
		else:
			await message.channel.send(f"{msg.content} is for the boys, now awaiting justins consent")

	elif "!whattimefortheboys" in message.content.lower():
		try:
			await message.channel.send(f"{msg.content} is for the boys, justins consent is {justinconsent}")
		except NameError:
			await message.channel.send("There is not yet a time for the boys")
	elif "!whytimefortheboys" in message.content.lower():
		await message.channel.send("because flirting with an e-girl does not count as human interaction")

	elif "!igottimefortheboys" in message.content.lower():
		readboyslist = open("theboysfile.txt", "r")
		boyslist = open("theboysfile.txt", "a")

		if message.author.name not in readboyslist.read():
			boyslist.write(f'{message.author.name},') 
			boyslist.close()
			readboyslist.close()
			await message.channel.send(f"{message.author.name} got time for the boys")
		else:
			boyslist.close()
			readboyslist.close()
			await message.channel.send("did you really want me to write your name twice?")

	elif "!whogottimefortheboys" in message.content.lower():
		try:
			readboyslist = open("theboysfile.txt", 'r')
			await message.channel.send(readboyslist.read())
			readboyslist.close()
		except discord.errors.HTTPException:
			await message.channel.send("Nobody got time for the boys :(")
	elif "!wheretheboysat" in message.content.lower():
		await message.channel.send("You do know that the title of this discord is Justin's Basement Bonanza, right?")

	elif "!noonesgottimefortheboys" in message.content.lower():
		clearboyslist = open("theboysfile.txt", 'w')
		clearboyslist.write("")
		clearboyslist.close()
		await message.channel.send("time has been cleared")

	
	elif "!whatsmyrole" in message.content.lower():
		await message.channel.send(message.author.roles)



	'''
		Best of _____ functionality:
			- send a message of form '!bestof(n, @Person)', where n is an odd number, and @Person is the tag of a user you want to challenge
			- At this point, the bot will create a text file to keep track of the games
			- The bot will ask for what game is being picked
			- Use the following elif's to tell the bot winners, get game info, etc.
	'''


	elif "!bestof(" in message.content.lower():
		try:
			num = int(message.content.lower()[8])
			gamecount = 0
			
			if (message.mentions == []):
				await message.channel.send("Looks like you forgot to include who you're challenging")
				return
			await message.channel.send("{} has challenged {} to a best of {}. Please pick the first game: ".format(message.author.name, message.mentions[0].name, num))
		except:
			await message.channel.send("An error has occurred; check that the message was properly formatted (i.e. bestof(int))")

		challengelist = [message.mentions[0],message.author]
		try:
			msg = await client.wait_for("message", timeout = 60)
		except:
			await message.channel.send("Challenge has expired")
		await message.channel.send("It's been decided. The first game will be: {}. Use '!win' to report the winner".format(msg.content))
		ongoinggame = open("bestof.txt", 'w')
		ongoinggame.write("{} {}\n".format(gamecount, num))
		ongoinggame.write("{} vs {}\n".format(challengelist[0].name, challengelist[1].name))
		ongoinggame.write("0 0\n")
		ongoinggame.write("{}\n".format(msg.content))
		ongoinggame.close()

	elif "!cleargame" in message.content.lower():
		try:
			score = game_info()
			await message.channel.send(score)
		except:
			await message.channel.send("No current game")
		game = open('bestof.txt', 'w')
		game.close()

	elif "!score" in message.content.lower():
		try:
			score = game_info()
			await message.channel.send(score)
		except:
			await message.channel.send("No current game")
	elif "!win" in message.content.lower():
		try: 
			winpos = 0
			currwin = 0
			otherwin = 0
			newgamescore = ""
			ongoinggame = open("bestof.txt", 'r')
			gameinfo = ongoinggame.readlines()
			ongoinggame.close()
			players = gameinfo[1].strip().split()
			if message.author.name == players[0]:
				winpos = 0
				winner = message.author.name
				currwin = int(gameinfo[2][0])
				otherwin = int(gameinfo[2][2])

				newgamescore = str(currwin + 1)
				newgamescore += gameinfo[2][1:]
				gameinfo[2] = newgamescore
			elif message.author.name == players[2]:
				winpos = 2
				winner = message.author.name
				currwin = int(gameinfo[2][winpos])
				otherwin = int(gameinfo[2][0])
				newgamescore = gameinfo[2][:2]
				newgamescore += str(currwin + 1) + '\n'
				
				gameinfo[2] = newgamescore
			else:
				await message.channel.send("Only current players can use !win")
				return


			ongoinggame = open("bestof.txt", 'w')
			for line in gameinfo:
				ongoinggame.write(line)
			ongoinggame.close()

			if (currwin + 1) >= ((int((gameinfo[0].strip().split())[1]) // 2) + 1):
				await message.channel.send("{} has won!".format(winner) + game_info())
				ongoinggame = open('bestof.txt', 'w')
				ongoinggame.close()
			else:
				if currwin == ((int((gameinfo[0].strip().split())[1]) // 2) + 1) and currwin == otherwin:
					await message.channel.send("A nail biter - I'm on the edge of my seat!")
				

				

				await message.channel.send("current " + game_info() + ". Please pick the next game: ")
				try:
					msg = await client.wait_for("message", timeout = 60)
				except:
					await message.channel.send("Challenge has expired. Clearing the game")
					ongoinggame = open('bestof.txt', 'w')
					ongoinggame.close()
				await message.channel.send("The next game will be: {}".format(msg.content))

			

		except:
			await message.channel.send("No current game")


	'''
		Rock, Paper, Scissors
			- Format message with '!rps @Person', where @Person is the tagged user you want to challenge
			- Bot will send DM's with instructions
	'''
	elif "!rps" in message.content.lower():
		if (message.mentions == []):
				await message.channel.send("Looks like you forgot to include who you're challenging")
				return
		else:
			await message.channel.send("{} has challenged {} to a game of rps!".format(message.author.name, message.mentions[0].name))
			player1 = message.author
			player2 = message.mentions[0]
			await player1.send("Please pick either rock, paper, or scissors")
			try:
				msg1 = await client.wait_for("message", timeout = 60)
			except:
				await message.channel.send("{} has forfeited the game by not choosing an option".format(message.author.name))
				return
			await player2.send("Please pick either rock, paper, or scissors")
			try:
				msg2 = await client.wait_for("message", timeout = 60)
			except:
				await message.channel.send("{} has forfeited the game by not choosing an option".format(message.mentions[0].name))
				return
			
			winstr = rps(msg1.content, msg2.content, player1.name, player2.name)

			await message.channel.send(winstr + "({} threw {}, {} threw {})".format(player1.name, msg1.content.lower(), player2.name, msg2.content.lower()))


	elif "!help" in message.content.lower():
		await message.channel.send("commands: (include ! in front) timefortheboys, whattimefortheboys, igottimefortheboys, whogottimefortheboys,whytimefortheboys, wheretheboysat")

'''
	REMOVED ON_TYPING METHOD:
		- Will send message if it finds that a user is typing
		- Quickly becomes extremely annoying

@client.event
async def on_typing(channel, user, when):
	await channel.send("Hey, whats the big idea, say it to my face!")'''


client.run(botToken)







