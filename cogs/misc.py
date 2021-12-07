import discord
from discord.ext import commands

class Miscellaneous(commands.Cog, name = "👻 Miscellaneous"): # Creating a class called Miscellaneous, for misc commands
    """
    Miscellaneous commands
    """
    def __init__ (self, bot): # Constructor Method
      self.bot = bot
    
    @commands.command(description="Displays the user's profile picture!", aliases = ["dp", "av", "pfp"]) 
    async def avatar(self, ctx, *, member: discord.Member=None): # Avatar command
        if member is not None:
            if isinstance(member, discord.Member) or isinstance(member, discord.User):
                pass
            else:
                member = ctx.author
        else:
            member = ctx.author # member is the user who sent the message
        avatarEmbed = discord.Embed(title=f"**{member}**'s Avatar", colour=discord.Color.from_rgb(241,210,231))
        avatarEmbed.set_thumbnail(url=URL)
        avatarEmbed.set_author(name="User Avatar", icon_url=ctx.author.avatar_url)
        await ctx.send(member.avatar_url) # Sends the of the member to post in chat
      
      
  """
    @commands.command(decription = "Changes the nickname for the tagged user within this server!", aliases = ["nickname", "changename", "name"])
    @commands.has_permissions(change_nickname=True)
    async def nick(ctx, member: discord.Member=None, *, nick=None): # Nickname command
        try:
            nick = ' '.join(nick)
        if nick is None:
            pass
        elif member is None:
            pass
        else:
            if (isinstance(member, discord.Member) or isinstance(member, discord.User)) and (len(nick.strip()) <= 32):
                original_nick = member.nick
                await member.edit(nick=nick) # member edits nickname
                await ctx.send(f"{member.mention}'s nickname has been changed from {original_nick} to {nick}.") # send in chat that nickname has been changed
  """    
      
      
def setup(bot):
  bot.add_cog(Miscellaneous(bot))
