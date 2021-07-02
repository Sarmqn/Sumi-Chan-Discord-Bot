import discord
from discord.ext import commands
from pretty_help import PrettyHelp, DefaultMenu

# --Load intents--
intents = discord.Intents.default()
intents.members = True

class SumiChan(commands.Bot):
    def __init__(self, command_prefix, help_command, description, **options):
        self.help_command = PrettyHelp(navigation=nav, color=discord.Colour.dark_purple())

bot = commands.Bot(command_prefix="sc!", case_insentive = True, description = "Nice handy bot that will help around", intents=intents) #Bot prefix
nav = DefaultMenu('◀️', '▶️', '❌')
bot.help_command =

@bot.event
async def on_ready():
    bot.load_extension("cogs.music")
    print("Ready to work haha") # Lets the bot owner know when the bot is ready
    
# --Load cogs--
cogs = [
    "moderation",
    "general",
]

for cog in cogs:
    bot.load_extension("cogs." + cog)
    print("Loaded: " + cog)

bot.load_extension("jishaku")
bot_token = 'NzkxMjkwMDg1MzU3MTI1NjMz.X-NAUQ.oYNL-1HvGbsPQERCskJB8tZj3wg'
bot.run(bot_token)