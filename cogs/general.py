import discord
from discord.ext import commands

# --Load intents--
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="sc!", case_insentive = True, description = "Nice handy bot that will help around", intents=intents) #Bot prefix

class General(commands.Cog):
    """
    General commands that server members can use
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'ping')
    async def ping(self, ctx):
        """
        Checks the current ping for the bot
        """
        await ctx.send(f'Pong! Bot latency is {round(self.bot.latency * 1000)}ms') # Says in chat what the current ping is and rounds it to the nearest whole number
    
    @commands.command(name='server')
    async def server_info(ctx: commands.Context):
        guild = ctx.guild
        await ctx.send(f'Server Name: {guild.name}')
        await ctx.send(f'Owner Name: {guild.owner.display_name}')
        await ctx.send(f'Server Size: {len(guild.members)}')
    
    @commands.Cog.listener()
    async def on_message(self, message):
         if message.content == "test":
                await message.channel.send("Testing 1, 2, 3!")
         if message.content == "hello":
                await message.channel.send("Hewo!")

def setup(bot):
    bot.add_cog(General(bot))

