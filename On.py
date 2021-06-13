import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu
from asyncio import sleep
import os
import random

bot = commands.Bot(command_prefix="sc!", case_insentive = True, description = "Nice handy bot that will help around") #Bot prefix

nav = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.DARK_VIVID_PINK)

@bot.event
async def on_ready():
    print("Ready to work haha") # Lets the bot owner know when the bot is ready

bot_token = os.environ.get("TOKEN")
bot.run(bot_token)
