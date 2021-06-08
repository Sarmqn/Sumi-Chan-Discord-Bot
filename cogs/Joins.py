import discord

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_messge_join(member):
    channel = client.get_channel(channel_id)
    embed.discord.Embed(title=f"Welcome {member.name}", description = f"Thanks for joining the server! {member.guild.name}!")
    embed.set_thumbnail(url=member.avata_url) # Embed's thumbnail = Users PFP

    await channel.send(embed=embed)
