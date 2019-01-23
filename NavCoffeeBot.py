import discord
import asyncio
import time
import requests
import threading
import os

from discord.ext.commands import bot
from discord.ext import commands

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

token = "ENTER YOUR BOT TOKEN HERE"
channel_id = "ENTER THE CHANNEL ID FOR THE BOT TO POST TO"

# Reports when bot is ready
@client.event
async def on_ready():
    print('NavCoffeeBot Ready')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('Invite URL: ' + 'https://discordapp.com/api/oauth2/authorize?client_id=' + client.user.id + '&permissions=8&scope=bot\n')
    
    # When bot is ready start reading wallet data
    update_wallet()

# Read up to date wallet data, compare to known wallet data
def update_wallet():
    threading.Timer(5.0, update_wallet).start()
	
    dono_file = open("/home/pi/Documents/donations2.txt", "r")
    donos = int(dono_file.readline())
    dono_file.close()
    
    bot_file = open("/home/pi/Documents/bot.txt", "r")
    bot_donos = int(bot_file.readline())
    bot_file.close()
    
    if donos > bot_donos:
        client.loop.create_task(send_update())
		
        bot_file_tmp = open("bot.txt.tmp", "w")
        bot_file_tmp.write(str(donos))
        bot_file_tmp.close()

        os.rename('bot.txt.tmp', 'bot.txt')

async def send_update():
    await client.wait_until_ready()
    await client.send_message(client.get_channel(channel_id), "Coffee Donated!")

# Run the bot
client.run(token)
