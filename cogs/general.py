
import discord
from discord.ext import commands
import discord

class General(commands.Cog):
    """
    General commands that server members can use
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'ping')
    async def ping(self, ctx: commands.Context):
        """
        Checks the current ping for the bot
        """
        embed = self.bot.embed(title="Pong!", description=f"Bot latency is {round(self.bot.latency * 1000)}ms") # this works because of the custom class
        await ctx.reply(embed=embed)

    @commands.command(name = 'nickname', aliases=["Nickname", "nick"])
    async def nickname(self, ctx, member: discord.Member, nick):
        """
        Helps user change nickname using command sc!nick or the aliases too
        """
        await member.edit(nick=nick)
        await ctx.send(f"{member.mention}'s nickname has been changed!") # prints and pings the user that changed nickname

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

