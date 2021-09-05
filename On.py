import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu
import os

# --Load intents--
intents = discord.Intents.default()
intents.members = True

class SumiChan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="sc!", description="Nice handy bot that will help around", intents=intents, help_command=None)

bot = SumiChan()

@bot.event
async def on_ready():
    print("Online") # Lets the bot owner know when the bot is ready
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='Matane!'))
# --Load cogs--
cogs = [
    "moderation",
    "general",
    "help"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)

    """
    
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
