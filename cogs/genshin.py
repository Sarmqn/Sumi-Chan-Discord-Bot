import discord, discord.utils, asyncio, os, json, requests
from discord import errors
from discord.ext import commands

colours = {"Anemo": discord.Color.from_rgb(166,245,207), "Cryo": discord.Color.from_rgb(189,254,254), "Dendro": discord.Color.from_rgb(176,233,36), "Electro": discord.Color.from_rgb(210,154,254), "Geo": discord.Color.from_rgb(247,214,98), "Hydro": discord.Color.from_rgb(12,228,252), "Pyro": discord.Color.from_rgb(255,167,104)}
suffixes = ["th", "st", "nd", "rd"] + (["th"]*6)
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
rarities = {"1": discord.Color.from_rgb(128,128,128), "2": discord.Color.from_rgb(30,255,0), "3": discord.Color.from_rgb(0,112,211), "4": discord.Color.from_rgb(163,53,238), "5": discord.Color.from_rgb(255,128,0)}

def make_ordinal(n: int):
    return f"{n}{suffixes[n%10]}"
def month_name(n: int):
    return months[n-1]


class Genshin(commands.Cog, name='<:GenshinImpact:905489184205197322> Genshin Impact'):
    """
    Trying out a Genshin API
    """
    def __init__(self, bot):
        self.bot = bot
    
    
    async def paging_system(embed, nopages, pagen, payload):
        user = self.bot.get_user(payload.user_id)
        if payload.emoji.name == "➡️":
            newpagen = pagen + 1
            if newpagen not in range(1, nopages+1):
                return None
            else:
                index = pagen
                if pagen == 1:
                    remove = ("➡️", user), ("➡️", self.bot)
                if 1 < newpagen and newpagen < nopages:
                    add = ("⬅️", "➡️")
                if newpagen == nopages:
                    remove = ("➡️", user), ("➡️", self.bot)
                    add = ("⬅️")
        else:
            newpagen = pagen - 1
            if newpagen not in range(1, nopages+1):
                return None
            else:
                index = pagen - 2
                if page_number == 3:
                    remove = ("⬅️", user)
                    add = ("➡️")
                elif page_number == 2:
                    remove = ("⬅️", self.bot), ("⬅️", user)
        if embed.title[:-6] == "Skills":
            response = requests.get(f"https://api.genshin.dev/characters/{embed.footer.text[:-9].lower().replace(' ', '-')}/")
            newpage = response.json()['skillTalents'][index]
            newEmbed = discord.Embed(title=f"{response.json()['name']}'s Skills", description=f"**{newpage['name']} ({newpage['unlock']})**\n{newpage['description']}", colour=colours[response.json()['vision']])
            newEmbed.set_footer(text=embed.footer.text[:-1]+str(newpagen))
            newEmbed.set_thumbnail(url=f"https://api.genshin.dev/characters/{character.lower()}/icon-big")
            try:
                upgrades = newpage['upgrades']
            except:
                pass
            else:
                upgradesText = ""
                for i in upgrades:
                    upgradesText += f"{i['name']}: {i['value']}\n"
                newEmbed.add_field(name="Upgrades", value=upgradesText, inline=False)
            return newEmbed, add, remove
        elif embed.title == "List of All Weapons":
            response = requests.get(f"https://api.genshin.dev/weapons/").json()
            weaponstr = ''
            for i in range(round(len(response)/2), len(response)):
                weaponstr = f"{response[i].replace('-s', '\'s').replace('-', ' ').title()} (`{response[i]}`), "
                newEmbed = discord.Embed(title='List of All Weapons', description=weaponstr, colour=discord.Color.from_rgb(241,210,231))
                newEmbed.set_footer(text=embed.footer.text[:-1]+str(newpagen))
            return newEmbed, add, remove
        else:
            return None
    
    
    
    @commands.group(invoke_without_command=True, aliases=['gi', 'g', 'genshinimpact', 'genshin_impact'], description='Get information about Genshin Impact! Use `sc!help genshin` for subcommands.')
    async def genshin(self, ctx):
      await ctx.reply('Genshin Impact is a free-to-play action RPG developed and published by miHoYo. The game features a fantasy open-world environment and action based combat system using elemental magic, character switching, and gacha monetization system for players to obtain new characters, weapons, and other resources. The game can only be played with an internet connection and features a limited multiplayer mode allowing up to four players in a world.\n\nUse `sc!help genshin` for subcommands!', mention_author=False)

    @commands.Cog.listener() # Listener for pagination
    async def on_raw_reaction_add(self, payload):
        # Get the message object they reacted to
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        # Check the bot is the author
        if (message.author.id == 773275097221169183) and (payload.user_id != 773275097221169183):
            if (payload.emoji.name == "➡️") or (payload.emoji.name == "⬅️"):
                try:
                    # Tries to retrieve the embed
                    embed = message.embeds[0]
                except Exception as e:
                    # If the embed doesn't exist (i.e. not a message we are interested in)
                    pass
                else:
                    response = None
                    if embed.title[-6:] == "Skills":
                        response = paging_system(embed, 3, int(embed.footer.text[-1]), payload)
                    elif embed.title == "List of All Weapons":
                        response = paging_system(embed, 2, int(embed.footer.text[-1]), payload)
            if response is None:
                pass
            else:
                newEmbed, add, remove = response
                if remove[0] != "➡️" or remove[0] != "⬅️":
                    for i in remove:
                        if i[0] != "➡️" or i[0] != "⬅️":
                                await message.remove_reaction(j[0], j[1])
                else:
                    await message.remove_reaction(remove[0], remove[1])
                for i in add:
                    await message.add_reaction(i)
                await message.edit(embed=newEmbed)
                
    
    @genshin.command(aliases=['ch', 'char'], description='Get character profiles.')
    async def character(self, ctx, character = None):
        if character is None:
            embed = discord.Embed(title='Character Profiles', description='Learn more about characters in Genshin! For a list of available characters use `sc!genshin characters`.')
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                rarity = ''
                for i in range(response.json()['rarity']):
                    rarity += '⭐'
                embed = discord.Embed(title=f"{character.capitalize()}'s Profile", description=f"{response.json()['description']}\n**Rarity:** {rarity}", colour=colours[response.json()['vision']])
                embed.set_thumbnail(url=f'https://api.genshin.dev/characters/{character}/icon-big')
                embed.add_field(name='Vision', value=response.json()['vision'], inline=True)
                embed.add_field(name='Weapon Type', value=response.json()['weapon'], inline=True)
                embed.add_field(name='Place of Origin', value=response.json()['nation'], inline=True)
                day = make_ordinal(int(response.json()['birthday'][-2:]))
                month = month_name(int(response.json()['birthday'][-5:-3]))
                embed.add_field(name='Birthday', value=f"{day} {month}", inline=True)
                embed.add_field(name='Skills', value=f'Use `sc!genshin skills {character}`', inline=True)
                embed.add_field(name='Affiliation', value=response.json()['affiliation'], inline=True)
                embed.add_field(name='Constellations', value=f"**{response.json()['constellation']}**\nUse `sc!genshin constellation {character}`", inline=True)
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Profiles', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the character command.\nArguments: {character}")
        embed.set_author(name='Character Profiles', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)


        
    @genshin.command(aliases=['chars', 'chs'], description="List of valid character names, sorted alphabetically.")
    async def characters(self, ctx):
        response = requests.get("https://api.genshin.dev/characters/").json()
        for i in range(len(response)):
            response[i] = response[i].capitalize()
        description = ', '.join(response)
        embed = discord.Embed(title='Available Characters', description=description, colour=discord.Color.from_rgb(241,210,231))
        await ctx.reply(embed=embed, mention_author=False)


    @genshin.command(aliases=['s', 'skill', 't', 'talents'], description="Look at a character's skills.")
    async def skills(self, ctx, character: str = None):
        if character is None:
            embed = discord.Embed(title='Character Skills', description="Learn about a Genshin characters' skills! For a list of available characters use `sc!genshin characters`.", colour=discord.Color.from_rgb(241,210,231))
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                skills = response.json()['skillTalents']
                embed = discord.Embed(title=f"{response.json()['name']}'s Skills", description=f"**{skills[0]['name']} ({skills[0]['unlock']})**\n{skills[0]['description']}", colour=colours[response.json()['vision']])
                try:
                    upgrades = skills[0]['upgrades']
                except:
                    upgradesText = None
                else:
                    upgradesText = ""
                    for i in upgrades:
                        upgradesText += f"{i['name']}: {i['value']}\n"
                if upgradesText is not None:
                    embed.add_field(name="Upgrades", value=upgradesText, inline=False)
                embed.set_footer(text=f"{character.capitalize()} | Page 1")
                embed.set_thumbnail(url=f"https://api.genshin.dev/characters/{character}/icon-big")
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Profiles', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the skills command.\nArguments: {character}")
        embed.set_author(name='Character Skills', icon_url=ctx.author.avatar_url)
        skillsEmbed = await ctx.reply(embed=embed, mention_author=False)
        if response.status_code == 200:
            await skillsEmbed.add_reaction("➡️")

    @genshin.command(aliases=['co', 'const'], description="Look at a character's constellation.")
    async def constellation(self, ctx, character: str):
        if character is None:
            embed = discord.Embed(title='Character Constellations', description="Learn about a Genshin characters' constellations! For a list of available characters use `sc!genshin characters`.", colour=discord.Color.from_rgb(241,210,231))
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                constellations = response.json()['constellations']
                embed = discord.Embed(title=f"{response.json()['name']}'s Constellations", colour=colours[response.json()['vision']])
                for i in constellations:
                    embed.add_field(name=f"{i['name']} ({i['unlock']})", value=i['description'])
                embed.set_thumbnail(url=f"https://api.genshin.dev/characters/{character}/icon-big")
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Constellations', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Constellations', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the constellation command.\nArguments: {character}")
        embed.set_author(name='Character Constellations', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)
    
            
        
    @genshin.command(aliases=['f'], description="Get information about food.")
    async def food(self, ctx, * food: str):
        food = ' '.join(food)
        response = requests.get("https://api.genshin.dev/consumables/food/").json()
        foodstr = ""
        if food == '':
            for i in response:
                foodstr += f"{response[i]['name']} (`{i}`), "
            foodstr = foodstr[:-2]
            embed = discord.Embed(title='List of All Food', description=foodstr, colour=discord.Color.from_rgb(241,210,231))
        else:
            try:
                fooddict = response[food.lower()]
            except KeyError:
                embed = discord.Embed(title=f"Food Info — {fooddict['name']}", description="This food doesn't exist, please make sure you typed it correctly!", colour=discord.Color.from_rgb(241,210,231))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                foodstr = f"{fooddict['description']}\n\n**Rarity:** "
                for i in range(fooddict['rarity']):
                    foodstr += '⭐'
                embed = discord.Embed(title=f"Food Info — {fooddict['name']}", description=foodstr, colour=discord.Color.from_rgb(241,210,231))
                embed.add_field(name='Food Type', value=fooddict['type'])
                embed.add_field(name='Effect', value=fooddict['effect'])
                embed.add_field(name='Proficiency', value=f"Cook {fooddict['proficiency']}x for Automatic Cooking.")
                if fooddict['hasRecipe'] == True:
                    recipe = ''
                    for i in fooddict['recipe']:
                        recipe += f"{i['quantity']}x {i['item']}\n"
                    embed.add_field(name='Ingredients', value=recipe)
                
        embed.set_author(name='Food Information', icon_url=ctx.author.avatar_url)    
        await ctx.reply(embed=embed, mention_author=False)

    @genshin.command(aliases=['p', 'pot', 'potion'], description="Get information about potions.")
    async def potions(self, ctx, * potion: str):
        potion = '-'.join(potion)
        response = requests.get("https://api.genshin.dev/consumables/potions/").json()
        potstr = ""
        if potion == '':
            for i in response:
                potstr += f"{response[i]['name']}, "
            potstr = potstr[:-2]
            embed = discord.Embed(title='List of All Potions', description=potstr, colour=discord.Color.from_rgb(241,210,231))
        else:
            try:
                potiondict = response[potion.lower()]
            except KeyError:
                embed = discord.Embed(title=f"Potion Info — {potion}", description="This potion doesn't exist, please make sure you typed it correctly!", colour=discord.Color.from_rgb(241,210,231))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                potstr = f"{potiondict['effect']}\n\n**Rarity:** "
                for i in range(potiondict['rarity']):
                    potstr += '⭐'
                embed = discord.Embed(title=f"Potion Info — {potiondict['name']}", description=potstr, colour=discord.Color.from_rgb(241,210,231))
                recipe = ''
                for i in potiondict['crafting']:
                    recipe += f"{i['quantity']}x {i['item']}\n"
                embed.add_field(name='Materials', value=recipe)
                
        embed.set_author(name='Potion Information', icon_url=ctx.author.avatar_url)    
        await ctx.reply(embed=embed, mention_author=False)

    @genshin.command(aliases=['e', 'element', 'r', 'reactions'], description="Find out more about elements and their reactions.")
    async def elements(self, ctx, * element: str):
        element = ' '.join(element).lower()
        if element == '':
            response = requests.get("https://api.genshin.dev/elements/").json()
            elementstr = ''
            for i in response:
                elementstr += f"{i.capitalize()}\n"
            embed = discord.Embed(title='List of All Elements', description=elementstr, colour=discord.Color.from_rgb(241,210,231))
        else:
            response = requests.get(f"https://api.genshin.dev/elements/{element}")
            if response.status_code == 404:
                embed = discord.Embed(title=f"Elemental Info — {element}", description="This element doesn't exist, please make sure you typed it correctly!", colour=discord.Color.from_rgb(241,210,231))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            elif response.status_code == 200:
                embed = discord.Embed(title=f"Elemental Info — {response.json()['name']}", colour=colours[element.capitalize()])
                for i in response.json()['reactions']:
                    embed.add_field(name=i['name'], value=f"{i['description']}\nElement(s): {', '.join(i['elements'])}", inline=True)
                embed.set_thumbnail(url=f"https://api.genshin.dev/elements/{element}/icon")
            else:
                embed = discord.Embed(title='Elemental Info', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the elemental info command.\nArguments: {element}")
        embed.set_author(name='Elemental Reactions', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @genshin.command(aliases=['w', 'weapon'], description="Learn about weapons' stats.")
    async def weapons(self, ctx, * weapon: str):
        weapon = '-'.join(weapon).lower()
        if weapon == '':
            response = requests.get("https://api.genshin.dev/weapons/").json()
            weaponstr = ''
            for i in response:
                weaponstr += f"{i}, "
            embed = discord.Embed(title='List of All Weapons', description=weaponstr, colour=discord.Color.from_rgb(241,210,231))
            embed.set_footer(text="Page 1")
        else:
            response = requests.get(f"https://api.genshin.dev/weapons/{weapon}")
            if response.status_code == 404:
                embed = discord.Embed(title=f"Weapon Info — {weapon}", description="This weapon doesn't exist, please make sure you typed it correctly!", colour=discord.Color.from_rgb(241,210,231))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            elif response.status_code == 200:
                response = response.json()
                embed = discord.Embed(title=f"Weapon Info — {response['name']}", colour=rarities[str(response['rarity'])])
                embed.add_field(name="Type", value=response['type'], inline=True)
                embed.add_field(name="Base Attack", value=response['baseAttack'], inline=True)
                embed.add_field(name="Sub Stat", value=response['subStat'], inline=True)
                embed.add_field(name="Passive Ability", value=f"**{response['passiveName']}**\n{response['passiveDesc']}", inline=True)
                embed.add_field(name="Unlock", value=response['location'].replace("Gacha", "Wishes"), inline=True)
                embed.set_thumbnail(url=f"https://api.genshin.dev/weapons/{weapon}/icon")
            else:
                embed = discord.Embed(title='Weapon Info', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the weapon info command.\nArguments: {weapon}")
        embed.set_author(name='Weapon Stats', icon_url=ctx.author.avatar_url)
        
        await ctx.reply(embed=embed, mention_author=False)
                    
                
                
def setup(bot):
    bot.add_cog(Genshin(bot))
