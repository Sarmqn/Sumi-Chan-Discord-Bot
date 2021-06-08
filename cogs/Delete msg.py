import discord from discord.ext
import async

async def on_message(message):
    if 'discord.gg' in message.content:
        await message.delete()
        await message.chnnel.send(f"{message.author.mention} This is forbidden to send!")
    else:
        await bot.process_commands(message)
        
