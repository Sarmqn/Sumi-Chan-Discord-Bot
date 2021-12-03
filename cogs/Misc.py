import discord
from discord.ext import commands

class Micellaneous (commands.Cog, name = "Miscellaneous"):
  """
  Miscellaneous commands
  """
  def __init__ (self, bot):
    self.bot = bot
    
    @commands.command(description="Displays the user's profile picture!")
    async def avatar(self, ctx, *, dp: discord.Member=None):
      URL = dp.avatar_url
      await ctx.send(URL)
      
    @commands.command(decription = "Changes the nickname for the tagged user within this server!")
    async def nick(ctx, nick, member: discord.Member=None):
      await member.edit(nick=nick)
      await ctx.send(f"{member.mention}'s nickname in {ctx.guild.name} has been changed")
      
      
      
def setup(bot):
  bot.add_cog(Miscellaneous(bot))
