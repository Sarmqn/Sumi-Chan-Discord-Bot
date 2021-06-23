import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu
from asyncio import sleep
import os
import random

# --Load intents--
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="sc!", case_insentive = True, description = "Nice handy bot that will help around", intents=intents) #Bot prefix
nav = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.dark_purple())

@bot.event
async def on_ready():
    print("Ready to work haha") # Lets the bot owner know when the bot is ready
    
# --Load cogs--
cogs = [
    "moderation",
    "general",
    "music"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)

# --Start bot--
bot_token = os.environ.get("TOKEN")
bot.run(bot_token)