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
activity = discord.CustomActivity(emoji="👋", name="Ohayou!", type="custom")
# activity = discord.Activity(type=discord.ActivityType.listening, name='Ohayo!')
bot_token = os.environ.get("TOKEN")
try:
    bot.run(bot_token, allowed_mentions = discord.AllowedMentions(everyone = False, roles = False), strip_after_prefix=True, case_insensitive=True, activity=activity, status=discord.Status.online)
except discord.errors.LoginFailure:
    print("Refresh the token! Matane!")
except Exception as e:
    print(e)

