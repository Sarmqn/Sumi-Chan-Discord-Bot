import discord
from discord.ext import commands

class Miscellaneous(commands.Cog, name = "👻 Miscellaneous"): # Creating a class called Miscellaneous, for misc commands
    """
    Miscellaneous commands
    """
    def __init__ (self, bot): # Constructor Method
      self.bot = bot
    
    @commands.command(description="Displays the user's profile picture!", aliases = ["dp", "av", "pfp"]) 
    async def avatar(self, ctx, member: discord.Member=None): # Avatar command
        if member is not None:
            if isinstance(member, discord.Member) or isinstance(member, discord.User):
                pass
            else:
                member = ctx.author
        else:
            member = ctx.author # member is the user who sent the message
        avatarEmbed = discord.Embed(title=f"**{member}**'s Avatar", colour=discord.Color.from_rgb(241,210,231))
        avatarEmbed.set_image(url=member.avatar_url)
        avatarEmbed.set_author(name="User Avatar", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=avatarEmbed) # Sends the of the member to post in chat
      
      

    @commands.command(description = "Changes the nickname for the tagged user within this server!", aliases = ["nickname", "changename", "name"])
    @commands.has_permissions(change_nickname=True)
    async def nick(self, ctx, member: discord.Member=None, *, nick=None): # Nickname command
        print(member)
        print(nick)
        try:
            nick = ' '.join(nick)
        except:
            pass
        else:
            if (nick is None) and (member is None):
                await ctx.send("Please mention a user and state a nickname!")
            elif (nick is None) or (nick is None):
                await ctx.send("Please specify a nickname!")
            else:
                if (isinstance(member, discord.Member) or isinstance(member, discord.User)) and (len(nick.strip()) <= 32):
                    original_nick = member.nick
                    await member.edit(nick=nick) # member edits nickname
                    await ctx.send(f"{member.mention}'s nickname has been changed from {original_nick} to {nick}.") # send in chat that nickname has been changed

      
      
def setup(bot):
  bot.add_cog(Miscellaneous(bot))
