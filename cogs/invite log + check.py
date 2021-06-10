import discord
from discord.ext import commands
import async

@bot.command(name='invite', description='Creates an invite link for the server')
async def invite(ctx, reason):
    invite = await ctx.guild.create_invite(reason=reason)
    await ctx.author.send(str(invite)) #This will send the invite link to the user who asked for it
    bot.dispatch('invite_command', invite)
    loggingchannel = bot.get_channel(channel_id)
    embed = discord.Embed(title= "New Invite", description=f"Invite created by {ctx.author}\nCode: {str(invite)}")
    await loggingchannel.send(embed=embed) #Logs who created the invite link

