
import discord
from discord.ext import commands

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

    @commands.command(name = 'nickname', aliases=["Nickname", "nick"])
    async def nickname(ctx, member: discord.Member, nick):
        """
        Helps user change nickname using command sc!nick or the aliases too
        """
        await member.edit(nick=nick)
        await ctx.send(f"{member.mention}'s nickname has been changed!") # prints and pings the user that changed nickname
    
    @commands.command(name='server')
    async def fetchServerInfo(context):
        guild = context.guild
        await context.send(f'Server Name: {guild.name}')
        await context.send(f'Owner Name: {guild.owner.display_name}')
        await context.send(f'Server Size: {len(guild.members)}')
        await context.send(f'Server ID: {id = str(ctx.guild.id)}')
    
    @bot.event
    async def on_message(message):
         if message.context == "test":
                await message.channel.send("Testing 1, 2, 3!")
         if message.context == "hello":
                await message.channel.send("Hewo!")
    
def setup(bot):
    bot.add_cog(General(bot))

