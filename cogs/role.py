import typing
import discord
from discord import mentions
from discord import reaction
from discord.enums import DefaultAvatar
from discord.ext import commands
from discord.raw_models import RawReactionClearEmojiEvent


class NotSetup(commands.CommandError):
    "An exception for when the reaction roles are not setup within a Discord Server (primarily my own)"
    pass


def setup():
    async def wrap_function(ctx):  # Wrapping function around command check for CTX
        info = await ctx.bot.config.find(
            ctx.guild.id
        )  # looking within the data base to see if it is setup
        if info is None:
            raise NotSetup

        if info.get("message_id") is None:
            raise NotSetup

        return True

    return commands.check(wrap_function)


class Reactions(commands.Cog, name="ReactionRoles"):
    def __init__(self, bot):
        self.bot = bot

    async def rebuild_role_embed(self, guild_id):
        info = await self.bot.config.find(guild_id)
        channel_id = info["channel_id"]
        message_id = info["message_id"]

        guild = await self.bot.fetch_guild(guild_id)
        channel = await self.bot.fetch_channel(channel_id)
        message = await self.bot.fetch_message(message_id)

        embed = discord.Embed(title="The Reaction Roles!")
        await message.clear_reactions()

        desc = ""
        reaction_roles = await self.bot.reaction_roles.get_all()
        reaction_roles = list(filter(lambda r: r["guild_id"] == guild_id, info))
        for item in reaction_roles:
            role = guild.get_role(item["role"])
            desc += f"{item['_id']}: {role.mention}\n"
            await message.add_reaction(item["_id"])

        embed.description = desc
        await message.edit(embed=embed)

    async def get_current_reactions(self, guild_id):
        info = await self.bot.reaction_roles.get_all()
        info = filter(lambda r: r["guild_id"] == guild_id, info)
        info = map(lambda r: r["_id"], info)
        return list(info)

    @commands.group(aliases=["rr", "reactionrole"], invoke_without_command=True)
    @commands.guild_only()
    async def reactionroles(self, ctx):
        await ctx.invoke(
            self.bot.get_command("help"), entity="reactionroles"
        )  # calling another command within the instance. Calling relevant commands

    @reactionroles.command(name="channel")  # Setting a channel
    @commands.guild_only()
    @commands.has_guild_permissions(
        manage_channels=True
    )  # Needing permissions within server to manage channels
    async def rr_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send(
                "No channel was given, hence I shall use the current channel I am within."
            )

        channel = channel or ctx.channel
        try:
            await channel.send(
                "Testing to see if I can send messages within this channel.",
                delete_after=10,
            )
        except discord.HTTPException:
            await ctx.send(
                "Sadly, I cannot send a message to that channel, please give me permissions to send a message and retry",
                delete_after=30,
            )
            return

        # database usage
        embed = discord.Embed(title="The Reaction Roles!")  # Reaction Role Embed

        desc = ""
        reaction_roles = await self.bot.reaction_roles.get_all()
        reaction_roles = list(
            filter(lambda r: r["guild_id"] == ctx.guild.id, reaction_roles)
        )  # Reference creation with everything needed, filter object
        for item in reaction_roles:
            role = ctx.guild.get_role(item["role"])
            desc += f"{item['_id']}: {role.mention}\n"
        embed.description = desc

        m = await channel.send(embed=embed)
        for item in reaction_roles:
            await m.add_reaction(item["_id"])  # Fetching role ID

        await self.bot.config.upsert(
            {
                "_id": ctx.guild.id,
                "message_id": m.id,
                "channel_id": m.channel.id,
                "is_enabled": True,
            }
        )
        await ctx.send("That should be setup now, enjoy!", delete_after=30)

        "Toggle Command"

    @reactionroles.command(name="toggle")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @setup()
    async def rr_toggle(self, ctx):
        """Toggleable reaction roles for the guild in use"""
        info = await self.bot.config.find(ctx.guild.id)
        info["is_enabled"] = not info["is_enabled"]  # flipped
        await self.bot.config.upsert(info)

        is_enabled = "Enabled." if info["is_enabled"] else "Disabled."
        await ctx.send(
            f"I have toggled that for you now! It is now currently {is_enabled}"
        )

    @reactionroles.command(name="add")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @setup()
    async def rr_add(
        self, ctx, emoji: typing.Union[discord.Emoji, str], *, role: discord.Role
    ):
        """Adding a new reaction role to users"""
        reacts = await self.get_current_reactions(ctx.guild.id)
        if len(reacts) >= 20:
            await ctx.send(
                "This does not support more than 20 reaction role per server! Sorry!"
            )
            return

        if not isinstance(emoji, discord.Emoji):
            emoji = emoji.get(emoji)
            emoji = emoji.pop()

        elif isinstance(emoji, discord.Emoji):
            if not emoji.is_usable():
                await ctx.send("I can't use that emoji sorry!")
                return

        emoji = str(emoji)
        await self.bot.reaction_roles.upsert(
            {"_id": emoji, "role": role.id, "guild_id": ctx.guild.id}
        )

        await self.rebuild_role_embed(ctx.guild.id)
        await ctx.send("That has been addde now and ready to be used!")

    @reactionroles.command(name="remove")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @setup()
    async def rr_remove(self, ctx, emoji: typing.Union[discord.Emoji, str]):
        """Remove an existing reaction role"""
        if not isinstance(emoji, discord.Emoji):
            emoji = emoji.get(emoji)
            emoji = emoji.pop()

        emoji = str(emoji)

        await self.bot.reaction_roles.delete(emoji)

        await self.rebuild_role_embed(ctx.guild.id)
        await ctx.send("I have removed this for you now!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        info = await self.bot.config.find(payload.guild_id)

        if not payload.guild_id or not info or not info.get("is_enabled"):

            guild_reaction_roles = await self.get_current_reactions(payload.guild_id)
        if str(payload.emoji) not in guild_reaction_roles:
            return

        guild = await self.bot.fetch_guild(payload.guild_id)

        emoji_data = await self.bot.reaction_roles.find(str(payload.emoji))
        role = guild.get_role(emoji_data["role"])

        member = await guild.fetch_member(payload.user_id)

        if role not in member.roles:
            await member.add_roles(role, reason="Reaction Role")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        info = await self.bot.config.find(payload.guild_id)

        if not payload.guild_id or not info or not info.get("is_enabled"):

            guild_reaction_roles = await self.get_current_reactions(payload.guild_id)
        if str(payload.emoji) not in guild_reaction_roles:
            return

        guild = await self.bot.fetch_guild(payload.guild_id)

        emoji_data = await self.bot.reaction_roles.find(str(payload.emoji))
        role = guild.get_role(emoji_data["role"])

        member = await guild.fetch_member(payload.user_id)

        if role in member.roles:
            await member.remove_roles(role, reason="Reaction Role")


def setup(bot):
    bot.add_cog(role(bot))


# But on the surface he looks calm and ready
