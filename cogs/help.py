import discord

@client.command()
async def plshelp(ctx, *hargs):
    hargs = ''.join(hargs)
    if (str(ctx.message.author.id) == '364045258004365312') or (str(ctx.message.author.id) == '389897179701182465'):
        if hargs == '':
            HelpEmbed=discord.Embed(title='Help for MinjuMail!', description='This message will self-destruct in 1 minute so as to not take up too much space.', color=random.choice(embedcolours))
            HelpEmbed.add_field(name="Admin", value="say\nshutdown", inline=True)
            HelpEmbed.add_field(name="Utility", value="reportabug", inline=True)
            HelpEmbed.add_field(name="Miscellaneous", value="ping\npong\nsnow", inline=True)
            HelpMessage = await ctx.send(embed=HelpEmbed)
        else:
            found = False
            for i in helplist:
                if i[0] == f'{hargs}':
                    index = helplist.index(i)
                    found = True
                    break
                else:
                    pass
            if found == False:
                HelpMessage = await ctx.send(embed=discord.Embed(title='Misspelling?', description=f'I could not find {hargs} command in the list of commands {ctx.author.mention}!'))
            else:
                HelpEmbed=discord.Embed(title=f"Help for '{hargs}'!", description='', color=random.choice(embedcolours))
                HelpEmbed.add_field(name="Description", value=f'{helplist[index][1]}', inline=False)
                HelpEmbed.add_field(name="Aliases", value=f'{helplist[index][2]}', inline=False)
                HelpEmbed.add_field(name="Command example", value=f'_{helplist[index][0]}', inline=False)
            HelpMessage = await ctx.send(embed=HelpEmbed)
        
        await ctx.message.delete()
        await asyncio.sleep(60)
        await HelpMessage.delete()
    else:
        pass
