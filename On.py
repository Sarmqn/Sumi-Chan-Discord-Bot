# --Importing all necessary libraries--
import discord, os, pymongo
from pymongo import MongoClient
from discord.ext import commands

# --Load intents--
intents = discord.Intents.default()
intents.members = True

# --Class for my bot Sumi-Chan--
class SumiChan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="sc!", description="Nice handy bot that will help around", intents=intents, help_command=None) # Super class
        self.id = 773275097221169183

bot = SumiChan()

@bot.event
async def on_ready(): # When the bot turns on
    print("https://www.youtube.com/watch?v=7uKcjGIxT-M") # Lets the bot owner know when the bot is ready, it will print out that it's "Roaring to go".
    await bot.change_presence(activity = discord.CustomActivity(emoji="👋", text="Ohayou!", type="custom")) # A Discord Rich Presense that will say the bot is playing "Matane!"
    "await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='Ohayo!'))" # A Discord Rich Presense that will say, commented out to try a new one

# --Loading all cogs--
cogs = [
    "moderation",
    "general",
    "genshin",
    "help"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)
    
    
"""
cluster = MongoClient("DBURL") # Using DBURL as the URL will be hidden as a secret
db = cluster["UserData"]
collection = db["UserData"]
 """ 
# --Start bot--
bot_token = os.environ.get("TOKEN")
try:
    bot.run(bot_token)
except discord.errors.LoginFailure:
    print("Refresh the token! Matane!")

