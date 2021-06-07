import os
import time
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="sumi!", case_insentive = True) #Bot prefix

@bot.event
asynd def on_ready():
    print("Ready to work") #Says in console whether bot is ready to recieve commands

        
bot.run('TOKEN') #Bot key code
