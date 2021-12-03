import discord
from discord.ext import commands

class Miscellaneous(commands.Cog, name = " 👻 Miscellaneous"): # Creating a class called Miscellaneous, for misc commands
  """
  Miscellaneous commands
  """
  def __init__ (self, bot): # Constructor Method
    self.bot = bot
    
  @commands.command(description="Displays the user's profile picture!", aliases = ["dp", "av", "pfp"]) 
  async def avatar(self, ctx, *, member: discord.Member=None): # Avatar command
    if not member: #If user is not a member
      member = ctx.author # member is the user who sent the message
    URL = member.avatar_url # Takes the url of the member's profile picture
    await ctx.send(URL) # Sends the url to post in chat
      
      
  """    
  @commands.command(decription = "Changes the nickname for the tagged user within this server!", aliases = ["nickname", "changename", "name"])
  async def nick(ctx, nick, member: discord.Member=None): # Nickname command
    await member.edit(nick=nick) # member edits nickname
    await ctx.send(f"{member.mention}'s nickname in {ctx.guild.name} has been changed") # send in chat that nickname has been changed
  """    
      
      
def setup(bot):
  bot.add_cog(Miscellaneous(bot))
