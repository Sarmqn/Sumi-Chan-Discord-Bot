from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'ping', description= "Checks the current ping")
    async def ping(self, ctx):
        await ctx.send(f'Pong! Bot latency is {round(self.bot.latency * 1000)}ms') # Says in chat what the current ping is and rounds it to the nearest whole number

def setup(bot):
    bot.add_cog(General(bot))
