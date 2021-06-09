import discord
from discord.ext import commands
from pretty_help import Navigation, PrettyHelp
from asyncio import sleep
import os
import random

bot = commands.Bot(command_prefix="sc!", case_insentive = True, description = "Nice handy bot that will help around") #Bot prefix
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.green()

@bot.event
async def on_ready():
    print("Ready to work haha") #Says in console whether bot is ready to recieve commands
def run():
    bot.run('TOKEN') #Bot token code
                              
if __name__ == "__main__":
  run()   
