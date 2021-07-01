import discord
from discord.ext import commands

class Ticket(commands.Cog):
  
  def __ini__(self, client):
    self.client = client
    
    @commands.command(name = "Ticket", aliases = "ticket")
    @commands.has_permission(administrator=True)
    async def Ticket(self, ctx):
      
      embed = discord.Embed(
        title = "Would you like to create a new ticket?",
        description = " If you have any questions or any concerns that bother you please create a new ticket by clicking on th emoji below.",
        colour=0xf7fcfd)
      
      embed.add_field(name = "Who do you want to report currently?", valkue =  value="Please contact a supporter or moderator directly!", inline=True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/771635939700768769/773121323341578250/external-content.duckduckgo.com.png")
        embed.set_author(name="Sumi-Chan-Tickets")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("📩")

def setup(client):
    bot.add_cog(Ticket(client))
