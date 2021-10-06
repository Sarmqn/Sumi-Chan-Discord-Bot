# --Importing all necessary libraries--
import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu
import os

# --Load intents--
intents = discord.Intents.default()
intents.members = True

# --Class for my bot Sumi-Chan--
class SumiChan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="sc!", description="Nice handy bot that will help around", intents=intents, help_command=None) # Super class

bot = SumiChan()

@bot.event
async def on_ready(): # When the bot turns on
    print("Roaring to go") # Lets the bot owner know when the bot is ready, it will print out that it's "Roaring to go".
    await bot.change_presence(activity = discord.Game(name="Matane!")) # A Discord Rich Presense that will say the bot is playing "Matane!"
    "await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='Matane!'))" # A Discord Rich Presense that will say, commented out to try a new one
"""
@bot.event
async def on_member_join(member): # References member as they join
    embed = discord.Embed(colour=discord.Colour.random), description = f"Welcome to Social Hub! You are the {len(list(member.guild.members))} member!!"
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/885197499319603242/895396695532265472/unknown.png")
    embed.add_field
"""
# --Loading all cogs--
cogs = [
    "moderation",
    "general",
    "help"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)

    """
#Database use currently commented out until finished    
if __name__ == "__main__":
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(Str(bot.connection_url))
    bot.db = bot.mongo["Documents"]
    bot.config = Document(bot.db, "config")
    bot.reaction_roles = Document(bot.db, "Reaction_Roles")
    
for file in os.listdir(cmd + "/cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"cogs.{file[:-3]}")
  
 """ 
  
# --Start bot--
bot_token = os.environ.get("TOKEN")
bot.run(bot_token)

# To drop bombs
