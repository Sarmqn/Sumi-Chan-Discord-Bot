import discord from discord.ext
import async

async def on_message(message):
    if 'discord.gg/' in message.content:
        await message.delete()
        await message.channel.send(f"This is forbidden to send {message.author.mention}!")
    else:
        await bot.process_commands(message)
        
