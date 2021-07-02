import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu
import os

# --Load intents--
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="sc!", case_insentive = True, description = "Nice handy bot that will help around", intents=intents) #Bot prefix
nav = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.dark_purple())

@bot.event
async def on_ready():
    print("Online") # Lets the bot owner know when the bot is ready
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='Matane!'))
# --Load cogs--
cogs = [
    "moderation",
    "general"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)

# --Start bot--
bot_token = os.environ.get("TOKEN")
bot.run(bot_token)
