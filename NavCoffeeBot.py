import discord
import asyncio
import time
import requests
import threading
import os

from discord.ext.commands import bot
from discord.ext import commands

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

token = "ENTER YOUR BOT TOKEN HERE"
channel_id = "ENTER THE CHANNEL ID THE BOT SHOULD OPERATE IN HERE"

# Reports when bot is ready
@client.event
async def on_ready():
    print('NavCoffeeBot Ready')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('Invite URL: ' + 'https://discordapp.com/api/oauth2/authorize?client_id=' + client.user.id + '&permissions=8&scope=bot\n')
    
    # When bot is ready start reading wallet data
    update_wallet()
    
# Message Listens / Commands
@client.event
async def on_message(message):
	
    # Give available coffee(s) on !coffee
    if message.content.upper() == "?COFFEE":
        coffee = get_coffees()
        redeems = get_redemptions()
        coffees_redeemable = str(coffee-redeems)
        reply = "There are " + coffees_redeemable + " coffees available for redemption! :coffee:"		
        await client.send_message(client.get_channel(channel_id), reply)

# Read coffees donated
def get_coffees():
    coffee_file = open("/home/pi/Documents/coffees_donated2.txt", "r")
    return int(coffee_file.readline())
    
# Read redemptions
def get_redemptions():
    redeem_file = open("/home/pi/Documents/redemptions2.txt", "r")
    return int(redeem_file.readline())

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
    await client.send_message(client.get_channel(channel_id), "Coffee Donated! :coffee:")

# Run the bot
client.run(token)
