import discord
from discord.ext import commands

class Logs(commands.Cog):
    """
    Moderation commands/listeners for log channels
    """
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 699909552757276732

    @commands.Cog.listener() # Delete msg if invite
    async def on_message(self, message):
        if not message.author.bot and 'discord.gg/' in message.content:
            await message.delete()
            await message.channel.send(f"This is forbidden to send {message.author.mention}!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.log_channel_id)
        JoinEmbed = discord.Embed(title=f"Welcome {member}", description = f"Thanks for joining {member.guild.name}!")
        JoinEmbed.set_thumbnail(url=member.avatar_url) # Embed's thumbnail = Users PFP
        await channel.send(embed=JoinEmbed)
        role = discord.utils.get(member.server.role, name='Member') #gets an object when given certain criteria and a source to look from
        await self.bot.add_roles(member, role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.log_channel_id)
        LeaveEmbed = discord.Embed(title=f"Byee {member}", description = f"Cya next time ;-( {member.guild.name}!")
        LeaveEmbed.se_thumbnail(url=member.avatar_url)
        await channel.send(embed=LeaveEmbed)
        
    @commands.command(name='invite')
    @commands.guild_only() # Restricts the command to the guild only
    async def invite(self, ctx):
        """
        Creates an invite link for the server
        """
        invite = await ctx.channel.create_invite()
        await ctx.author.send(str(invite)) #This will send the invite link to the user who asked for it
        loggingchannel = self.bot.get_channel(self.log_channel_id)
        embed = discord.Embed(title= "New Invite", description=f"Invite created by {ctx.author}\nCode: {str(invite)}")
        await loggingchannel.send(embed=embed) #Logs who created the invite link
        
        #  ---BAN---
        
    @commands.command('ban')
    async def ban(ctx: commands.Context, member: discord.Member):
        if member == ctx.guild.me:
            return await ctx.send("Nice try")
        if member.guild_permissions.administrator==True:
            return await ctx.send("Whoops! You can't ban them...")
        else:
            await member.send(f"{ctx.author} Banned")
            await member.ban()
            
        #  ---MUTE---    
            
    @commands.command('mute') # Mute command
    async def mute(ctx: commands.Context, member: discord.Member):
        role_members = discord.utils.get(ctx.guild.roles, name='Members')
        role_muted = discord.utils.get(ctx.guild.roles, name='Members')
        await member.remove_roles(role_members)
        await member.add_roles(role_muted)
        await context.send("User Was Muted")
            
        #  ---UNMUTE---    
            
    @commands.command('unmute') # Unmute command
    async def unmute(ctx, member: discord.Member):
        role_members = discord.utils.get(ctx.guild.roles, name='Members')
        role_muted = discord.utils.get(ctx.guild.roles, name='Members')
        await member.remove_roles(role_muted)
        await member.add_roles(role_members)
        await context.send("User Was Unmuted")



def setup(bot):
    bot.add_cog(Logs(bot))
