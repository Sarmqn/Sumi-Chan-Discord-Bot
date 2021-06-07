import discord
from discord.ext import commands
import async

@bot.command(name='invite', description='Creates an invite link for the server')
async def invite(ctx, reason):
    invite = await ctx.guild.create_invite(reason=reason)
    await.ctx.author.send(str(invite)) #This will send the invite link to the user who asked for it
    invite.inviter = ctx.author
    bot.dispatch('invite_command', invite)

@bot.event
async def on_invite_command(invite):
    channel = bot.get_channel(channel_id)
    embed = discord.Embed(title= "New Invite", description=f" Invite created by {invite.inviter}\nCode: {str(invite)}")
    await channel.send(embed=embed) #Logs who creates invite links
