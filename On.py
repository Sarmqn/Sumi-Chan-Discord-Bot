# --Importing all necessary libraries--
import discord, os, pymongo
from pymongo import MongoClient
from discord.ext import commands

# --Load intents--
intents = discord.Intents.all()

# --Class for my bot Sumi-Chan--
activity = discord.Activity(type=3, name="Rent-A-Girlfriend", url="https://www.youtube.com/watch?v=-v8M0KNgKwY", application_id=869328857734451250, details="Watch me!", assets={"large_image": "sumi", "large_text": "Blushing", "small_image": "youtube", "small_text": "Youtube"})
activity = discord.Activity(type=3, name="Rent-A-Girlfriend", url="https://www.youtube.com/watch?v=-v8M0KNgKwY", application_id=839885828510580756, details="Watch me!", large_image_url="https://cdn.discordapp.com/attachments/678552360905211934/915691811937349662/541ab3dd58502e78d64a863cb3c5e368.png", large_image_text="Blushing", small_image_url="https://www.youtube.com/s/desktop/1b183e4b/img/favicon.ico", small_image_text=="Youtube")
# activity = discord.Activity(type=discord.ActivityType.listening, name='Ohayou!')
class SumiChan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="sc!", description="Nice handy bot that will help around", intents=intents, help_command=None, allowed_mentions = discord.AllowedMentions(everyone = False, roles = False), strip_after_prefix=True, case_insensitive=True, activity=activity, status=discord.Status.online) # Super class
        self.id = 869328857734451250

bot = SumiChan()

@bot.event
async def on_ready(): # When the bot turns on
    print("https://www.youtube.com/watch?v=7uKcjGIxT-M") # Lets the bot owner know when the bot is ready, it will print out that it's "Roaring to go".

@bot.command()
@commands.is_owner()
async def testactiv(ctx, id: int):
    print(ctx.guild.get_member(id).activities)
    for i in ctx.guild.get_member(id).activities:
        print(i.type)
        print(i.assets)


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
except Exception as e:
    print(e)

