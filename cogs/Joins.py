import discord

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_messge_join(member):
    channel = client.get_channel(channel_id)
    JoinEmbed = discord.Embed(title=f"Welcome {member}", description = f"Thanks for joining {member.guild.name}!")
    JoinEmbed.set_thumbnail(url=member.avata_url) # Embed's thumbnail = Users PFP

    await channel.send(embed=JoinEmbed)
