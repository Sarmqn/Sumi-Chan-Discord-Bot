# --Importing all necessary libraries--
import discord, os
from discord.ext import commands

# --Load intents--
intents = discord.Intents.all()

# --Class for my bot Sumi-Chan--
activity = discord.Streaming(name="Rent-A-Girlfriend", url="https://www.youtube.com/watch?v=-v8M0KNgKwY")
# activity = discord.Activity(type=discord.ActivityType.listening, name='Ohayou!')
class SumiChan(commands.Bot):
    def __init__(self):
        # Calling the __init__ (constructor) function of the superclass (commands.Bot) with given parameters
        super().__init__(command_prefix="sc!", description="Nice handy bot that will help around", intents=intents, help_command=None, allowed_mentions = discord.AllowedMentions(everyone = False, roles = False), strip_after_prefix=True, case_insensitive=True, activity=activity, status=discord.Status.online)
        self.id = 869328857734451250

bot = SumiChan()

@bot.event
async def on_ready(): # When the bot turns on
    print("Ohayou senpai!") # Lets the bot owner know when the bot is ready, it will print out "Ohayou senpai!".


# --Loading all cogs--
cogs = [
    "entertainment",
    "general",
    "genshin",
    "help",
    "misc",
    "moderation"
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)
    

# --Start bot--

bot_token = os.environ.get("TOKEN")
try:
    bot.run(bot_token)
except discord.errors.LoginFailure as e:
    print(f"Can't login! Matane...\n{e}")
except Exception as e:
    print(e)

