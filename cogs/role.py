import discord
from discord.ext import commands

class rr(commands.cog):
  def __init__(self, ctx, bot):
    self.bot = bot
  
  @commands.command()
  async def on_raw_reaction_add(self, ctx, payload):
    message_id = payload.message_id
    if message_id = "":
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
      role = discord.utils.get(guild.roles, name =
    
    
    
  @commands.command()
  async def on_raw_reaction_remove( 
