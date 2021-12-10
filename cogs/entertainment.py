import discord
from discord.ext import commands
import random

SlapGIFs = [""]
HugGIFs = ["https://giphy.com/clips/parksandrec-parks-and-recreation-rec-peacock-tv-cU14kx6qeHqaTK6ZeJ"]
KissGIFs = [""]
SmilingGIFs = [""]
TickleGIFs = [""]
PunchGIFs = [""]


class Entertainment(commands.Cog, name="💣 Entertainment"):
    """
    General commands that server members can use
    """
    def __init__(self, bot): # Defining the constructor method
        self.bot = bot
    
    async def user_check(self, user):
        if (user is None) or (not isinstance(user, discord.Member)) or (not isinstance(user, discord.User)):
            return "themselves"
        else:
            return user.mention
    
    
    @commands.command(description="Slap a user!")
    async def slap(self, ctx, *, user: discord.Member=None):
        print(type(user))
        user = await self.user_check(user)
        slapEmbed = discord.Embed(title= "Ouch!", description=f"{ctx.author} slapped {user}!", colour=discord.Color.from_rgb(241,210,231))
        slapEmbed.set_thumbnail(url=random.choice(slapGIFs))
        await ctx.reply(embed=slapEmbed, mention_author=False)
    
    
    """
    --- WIP---
    @commands.command(description = "Hugs the tagged user!")
    async def hug(self, ctx, *, user:discord.Member=None):
        user = await self.user_check(user)
        hugEmbed = discord.Embed(title = "Awww, here's a hug!", descrpton = "Hugs", format(user, ctx.message.author.name), color=FFB6C1)
        hugEmbed.set_thumbnail(url=random.choice(HugGIFs)
        await ctx.reply(embed=HugEmbed, mention_author=False)
    
    @commands.command(description = "Kisses the tagged user!")
    async def kiss(self, ctx, *, user:dicsord.Member=None):  
        user = await self.user_check(user)
        
        
        await ctx.reply(embed=, mention_author=False)

        
    @commands.command(description = "Smiles at the tagged user!")
    async def smile(self, ctx, *, user:discord.Member=None):  
        user = await self.user_check(user)
        
        
        await ctx.reply(embed=, mention_author=False)
    
    @commands.command(description = "Tickles the tagged user!")
    async def tickle(self, ctx, *, user:discord.Member=None):  
        user = await self.user_check(user)
        
        
        await ctx.reply(embed=, mention_author=False)
    
    @commands.command(aliases = ['handhold', 'hh'], description = "Holds Hands with the tagged user!")
    async def holdhands(self,ctx, *, user:discord.Member=None): 
        user = await self.user_check(user)
        
        
        await ctx.reply(embed=, mention_author=False)
    
    @commands.command(aliases = ['hit', 'fist'], description = "Punch the tagged user!")
    async def punch(self,ct, *, user:discord.Member=None):
        user = await self.user_check(user)
        
        await ctx.reply(embed =, mention_author=False)
    
    
    
"""

def setup(bot):
    bot.add_cog(Entertainment(bot))
