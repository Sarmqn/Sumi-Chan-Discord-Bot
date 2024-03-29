import discord, asyncio
from discord import *
from discord.ext import commands

class Moderation(commands.Cog, name='🛠️ Moderation'): # Creates a class called "Logs" as a subclass of commands.Cog
    """
    Moderation commands/listeners for log channels
    """
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 699909552757276732 # Channel ID of where everything will be logged

    @commands.Cog.listener() # Detect discord.gg invite links and delete them.
    async def on_message(self, message): #When the message is sent
        if (not (message.author.bot or message.author.id == 701817552778559510)) and ('discord.gg/' in message.content) or ('discord.com/invite/' in message.content): # that includes discord.gg/
            log_channel = self.bot.get_channel(699909552757276732)
            await message.delete() # Delete that message 
            await message.channel.send(f"Don't send server invites in this server {message.author.mention}!") # And reply stating that these invites should not be sent in chat
            await log_channel.send(f'{message.author.mention} (`{message.author.id}`) sent an invite in {message.channel.mention}.') # Pings that the user to let them know

    @commands.Cog.listener()
    async def on_member_join(self, member):
        gen_channel = self.bot.get_channel(678356960151863340)
        JoinEmbed = discord.Embed(title=f"Welcome {member}!", description = f"Thanks for joining {member.guild.name}! We hope you enjoy your stay!\nGo to <#715859030039330847> for some roles!")
        JoinEmbed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to be the user's profile picture.
        msg = await gen_channel.send(member.mention, embed=JoinEmbed)
        await msg.add_reaction("🎉")
        role = discord.utils.get(member.guild.roles, id=678551601740251136) # Gets the role object given an ID and list
        await member.add_roles(role) # Gives new user the aforementioned role

    @commands.Cog.listener()
    async def on_member_remove(self, member): #When a member leaves / is removed from the server
        log_channel = self.bot.get_channel(699909552757276732)
        LeaveEmbed = discord.Embed(title=f"See you next time, {member}", description = f"Thanks for being a part of {member.guild.name}!") #Send a nice embed
        LeaveEmbed.set_thumbnail(url=member.avatar_url) # Users profile picture as thumbnail
        await log_channel.send(embed=LeaveEmbed) # Send in the logs channel 
        
        #  ---BAN---
    @commands.command(aliases = ['goaway'], description="Ban a user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, * reason: str):
        log_channel = self.bot.get_channel(699909552757276732)
        if isinstance(member, discord.Member): # Checks if the argument passed was a discord.Member object.
            pass
        elif isinstance(member, int):
            member = self.bot.get_user(member)
            if member is None: # If the ID is invalid
                await ctx.send("That isn't a valid member ID.")
        else:
            await ctx.send('Not an ID/mention. Try again.')
            member = None
        # If they are trying to ban the bot
        if member is ctx.guild.me:
            return await ctx.send("Nice try")
        # If they are trying to ban someone with administrator permissions
        if member.guild_permissions.administrator==True:
            return await ctx.send("Whoops! You can't ban them...")
        else:
            if member is None:
                pass
            else:
                reason = str(reason)
                if reason == '()' or reason==():
                    reason = 'N/A'
                await member.send(f"You were banned from **{ctx.guild}** by **{ctx.author}**.\nReason: {reason}.")
                await ctx.send(f"{member} has been banned.")
                await log_channel.send(f"{member} has been banned by {ctx.author}.\nReason: {reason}.")
                await member.ban(reason=reason)
                
        #  ---MUTE---    
    @commands.command(aliases = ['shutup', 'quiet'], description="Mute a user.") # Mute command
    @commands.has_permissions(manage_messages=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        log_channel = self.bot.get_channel(699909552757276732)
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        if role_muted in member.roles:
            await ctx.send(f'**{member}** is already muted.')
        else:
            role_members = discord.utils.get(ctx.guild.roles, name='Member')
            await member.remove_roles(role_members, reason=f"User muted by {ctx.author}")
            await member.add_roles(role_muted, reason=f"User muted by {ctx.author}.")
            await ctx.send(f"**{member}** was muted.")
            await log_channel.send(f"**{member}** has been muted by {ctx.author.mention}")

               
        #  ---UNMUTE---    
    @commands.command(description="Unmute a user.") # Unmute command
    @commands.has_permissions(manage_messages=True, manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        log_channel = self.bot.get_channel(699909552757276732)
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        if role_muted in member.roles:
            role_members = discord.utils.get(ctx.guild.roles, name='Member')
            await member.remove_roles(role_muted, reason=f"User unmuted by {ctx.author}.")
            await member.add_roles(role_members, reason=f"User unmuted by {ctx.author}.")
            await ctx.send(f"**{member}** was unmuted.")
            await log_channel.send(f"**{member}** has been unmuted by {ctx.author.mention}")
        else:
            await ctx.send(f'**{member}** is not muted.')

        # ---UNBAN---
    @commands.command(aliases = ['comeback'], description="Unban a user.") #Unban command
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int, * reason: str):
        log_channel = self.bot.get_channel(699909552757276732)
        userID = await self.bot.fetch_user(id) # Gets user's ID
        try:
            await ctx.guild.unban(userID, reason=reason)
        except discord.errors.NotFound:
            await ctx.send('User is not banned!')
        else:
            if reason == () or reason == ():
                reason = 'N/A'
            await ctx.send(f'**{userID}** has been unbanned.\nReason: {reason}.')
            await log_channel.send(f"**{member}** has been unbanned by {ctx.author.mention}")
        
        # ---KICK---
    @commands.command(aliases = ['remove', 'bye'], description="Kick a user.") # Kicks a user that is mentioned
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, * reason: str):
        log_channel = self.bot.get_channel(699909552757276732)
        if isinstance(user, discord.Member):
            await user.kick(reason=reason)
        elif isinstance(user, int) or isinstance(user, str):
            user = guild.get_member(int(userid))
        await ctx.message.add_reaction("👌")
        await ctx.send(f"**{user}** was kicked by {ctx.author.name}!")
        await user.send(f"You were kicked from **{ctx.guild}** by **{ctx.author}**.")
        await user.kick(reason=reason)
        await log_channel.send(f"**{member}** has been kicked by {ctx.author.mention}")
                               
        # ---PURGE---
    @commands.command(aliases = ['delete'], description="Purge messages in a channel.") # Purge command
    @commands.has_permissions(manage_messages=True) # checks for manage message perms for the user who uses it        
    async def purge(self, ctx, amount: int):
        if isinstance(amount, int):
            log_channel = self.bot.get_channel(699909552757276732)
            await ctx.message.delete() # Deletes messages using the command prefix and the parameter
            purgemsg = await ctx.channel.purge(limit=int(amount))
            deletemsg = await ctx.send(f"{len(purgemsg)} messages have been deleted from the channel!", delete_after=5) # prints a message stating that the messages have been purged that will be deleted after 5 seconds
            if purgemsg != []:
                logmsg = ''
                for i in purgemsg:
                    logmsg += f"{i.author}: {i.content}\n"
            else:
                logmsg = 'None.'
            await log_channel.send(f"{ctx.author.mention} purged {len(purgemsg)} messages in {ctx.channel}.\n\n{logmsg}")
                                           
def setup(bot):
    bot.add_cog(Moderation(bot))
