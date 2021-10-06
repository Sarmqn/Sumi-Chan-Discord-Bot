import discord
from discord import errors
from discord.ext import commands
import discord.utils
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Logs(commands.Cog):  # Creates the class with an instance of Logs
    """
    Moderation commands/listeners for log channels
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = 699909552757276732
        self.log_channel = bot.get_channel(699909552757276732)

    @commands.Cog.listener()  # Delete any invite links from the chat
    async def on_message(self, message: discord.Message):
        if (
            not message.author.bot
            and ("discord.gg/" in message.content)
            or ("discord.com/invite/" in message.content)
        ):
            await message.delete()
            await message.channel.send(
                f"Don't send server invites in this server {message.author.mention}!"
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        JoinEmbed = discord.Embed(
            title=f"Welcome {member}",
            description=f"Thanks for joining {member.guild.name}!",
        )
        JoinEmbed.set_thumbnail(url=member.avatar_url)  # Embed's thumbnail = Users PFP
        await self.log_channel.send(embed=JoinEmbed)
        role = discord.utils.get(
            member.guild.roles, id=678551601740251136
        )  # gets an object when given certain criteria and a source to look from
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        LeaveEmbed = discord.Embed(
            title=f"See you next time, {member}",
            description=f"Thanks for being a part of {member.guild.name}!",
        )
        LeaveEmbed.set_thumbnail(url=member.avatar_url)
        await self.log_channel.send(embed=LeaveEmbed)

    @cog_ext.cog_slash(name="invite")
    async def invite(self, ctx: SlashContext):
        """
        Creates an invite link for the server
        """
        if (
            ctx.channel.type == discord.ChannelType.private
        ):  # Restricts the command to the guild only
            return
        invite = await ctx.channel.create_invite(
            reason=f"{ctx.author} used the invite command.", max_uses=1, unique=True
        )
        await ctx.author.send(
            str(invite)
        )  # This will send the invite link to the user who asked for it
        embed = discord.Embed(
            title="New Invite",
            description=f"Invite created by {ctx.author}\nCode: {str(invite)}",
        )
        await self.log_channel.send(embed=embed)  # Logs who created the invite link

        #  ---BAN---

    @cog_ext.cog_slash(
        "ban",
        options=[
            create_option(
                name="member",
                description="The member to ban",
                option_type=6,  # Option type: member
                required=True,
            )
        ],
    )
    async def ban(self, ctx: SlashContext, member: discord.Member):
        if ctx.author.guild_permissions.ban_members == True:
            if isinstance(member, discord.Member):
                pass
            elif isinstance(member, int):
                member = self.bot.get_user(member)
            else:
                await ctx.send("Not an ID/mention. Try again.")
                member = None
            # If they are trying to ban the bot
            if member == ctx.guild.me:
                return await ctx.send("Nice try")
            if member.guild_permissions.administrator == True:
                return await ctx.send("Whoops! You can't ban them...")
            else:
                if member == None:
                    pass
                else:
                    await member.send(
                        f"You were banned from **{ctx.guild}** by **{ctx.author}**."
                    )
                    await ctx.send(f"{member} has been banned.")
                    await self.log_channel.send(
                        f"{member} has been banned by {ctx.author}."
                    )
                    await member.ban()

        #  ---MUTE---

    @cog_ext.cog_slash(
        "mute",
        options=[
            create_option(
                name="member",
                description="The member to mute",
                option_type=6,  # Option type: member
                required=True,
            )
        ],
    )  # Mute command
    async def mute(self, ctx: SlashContext, member: discord.Member):
        if ctx.author.guild_permissions.administrator == True:
            role_muted = discord.utils.get(ctx.guild.roles, name="Muted")
            if role_muted in member.roles:
                await ctx.send(f"**{member}** is already muted.")
            else:
                role_members = discord.utils.get(ctx.guild.roles, name="Member")
                await member.remove_roles(role_members)
                await member.add_roles(role_muted)
                await ctx.send(f"**{member}** was muted.")

        #  ---UNMUTE---

    @cog_ext.cog_slash(
        "unmute",
        options=[
            create_option(
                name="member",
                description="The member to unmute",
                option_type=6,  # Option type: member
                required=True,
            )
        ],
    )  # Unmute command
    async def unmute(self, ctx: SlashContext, member: discord.Member):
        if ctx.author.guild_permissions.administrator == True:
            role_muted = discord.utils.get(ctx.guild.roles, name="Muted")
            if role_muted in member.roles:
                role_members = discord.utils.get(ctx.guild.roles, name="Member")
                await member.remove_roles(role_muted)
                await member.add_roles(role_members)
                await ctx.send(f"**{member}** was unmuted.")
            else:
                await ctx.send(f"**{member}** is not muted.")

    @cog_ext.cog_slash(
        "unban",
        options=[
            create_option(
                name="member",
                description="The member to ban",
                option_type=6,  # Option type: member
                required=True,
            )
        ],
    )  # Unban command
    async def unban(self, ctx: SlashContext, uid: int):
        if ctx.author.guild_permissions.ban_members == True:
            userID = await ctx.self.bot.fetch_user(id)  # Gets users ID
            try:
                await ctx.guild.unban(userID)
            except discord.errors.NotFound:
                await ctx.send("User is not banned!")
            else:
                await ctx.send(f"**{userID}** has been unbanned.")
        else:
            await ctx.send("Uh oh, I don't have permissions!")

    @cog_ext.cog_slash(
        "kick",
        options=[
            create_option(
                name="member",
                description="The member to kick",
                option_type=6,  # Option type: member
                required=True,
            )
        ],
    )  # Kicks a user that is mentioned
    async def kick(self, ctx: SlashContext, member: discord.Member):
        if (
            ctx.author.guild_permissions.kick_members == True
            or ctx.author.guild_permissions.administrator == True
        ):
            if isinstance(member, discord.Member):
                await member.kick()
            elif isinstance(member, int) or isinstance(member, str):
                member = ctx.guild.get_member(member.id)
                await member.kick()
            await ctx.message.add_reaction("👌")
            await ctx.send(f"{member.name} was kicked by {ctx.author.name}!")
            await member.send(
                f"You were kicked from **{ctx.guild}** by **{ctx.author}**."
            )
        else:
            return await ctx.send("I'm missing the `KICK_MEMBERS` permission!")

    """
    @cog_ext.cog_slash('purge') # Purges a channel based on where it is used.
    async def purge(self, ctx):
        if ctx.author.guild_permissions.administrator:
       """


def setup(bot):
    bot.add_cog(Logs(bot))


# Mom's spagghetti
