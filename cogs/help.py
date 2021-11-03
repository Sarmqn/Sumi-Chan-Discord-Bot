# Import required libraries
import discord
from datetime import datetime
from discord.ext import commands
import random

# Set necessary variables
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]

# Set atributes for the help command
attributes = {
   'name': "help",
   'aliases': ["h"],
   'description': "Get help with commands."
}


# Create class for help message based off the default one, here I'm overwriting existing functions.
class MyHelp(commands.HelpCommand):
    """Get help with commands!"""
    # ^ Docstring.
   
    # Used to get the 'signature'/usage of a command, i.e. `_help`
    def get_command_signature(self, command):
        # Checks if there are required/optional arguments
        if command.signature == '':
            return '`{0.clean_prefix}{1.qualified_name}`'.format(self, command)
        else:
            return '`{0.clean_prefix}{1.qualified_name}` `{1.signature}`'.format(self, command)
    
    # Used when someone only does `_help`
    async def send_bot_help(self, mapping):
        # Generate embed
        embed = discord.Embed(title="Help", color=random.choice(embedcolours))
        # For each cog and it's associated list of commands in `mapping.items`...
        for cog, commands in mapping.items():
            # Filter out the commands that the user isn't allowed to use and sort them alphabetically
            filtered = await self.filter_commands(commands, sort=True)
            # Put the signatures of those commands into an array (search 'List Comprehension' for this format)
            command_signatures = [self.get_command_signature(command) for command in filtered]
            # If a value is returned (since `None` will be returned if nothing is found)
            if command_signatures:
                # Get the attribute `qualified_name` of cog, putting "Miscellaneous" if not found
                cog_name = getattr(cog, "qualified_name", "Miscellaneous")
                # Adds an inline field with title of cog name and value of command signatures.
                embed.add_field(name=f'{cog_name}', value="\n".join(command_signatures), inline=True)
        # More embed generation
        embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
        # Send the embed as a reply
        await self.context.reply(embed=embed)
                
    # Used when someone does "_help <cog name>"
    async def send_cog_help(self, cog):
        # Get an array of commands
        commands = [command for command in cog.get_commands()]
        # Get a filtered version of commands
        filtered = await self.filter_commands(commands, sort=True)
        # Get an array of command signatures
        command_signatures = [self.get_command_signature(c) for c in filtered]
        # Sets embed description to `None`
        desc = None
        # Checks if anything was returned
        if command_signatures:
            # Joins the array line by line
            desc = '\n'.join(command_signatures)
            # Embed generation
            embed = discord.Embed(title=f'{cog.qualified_name[2:]} Help', description=f'**{cog.__doc__}**\n\n{desc}', color=random.choice(embedcolours))
            embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
            # Send embed as a reply
            await self.context.reply(embed=embed)
        # If nothing was returned, i.e. user doesn't have access to use that cog
        else:
            await self.context.reply(f'No category called "{cog.qualified_name}" found.')
    
    # Used when someone does "_help <group name>", such as "_help suggest".
    async def send_group_help(self, group):
        # Get an array of command signatures. There is no filter check since the only groups I plan to use will be available to everyone
        command_signatures = [self.get_command_signature(command) for command in group.commands]
        # Gets the part to remove from each signature to only get the subcommand name
        tostrip = f'_{group.name} '
        # Since subcommands are required, begin the arguments (`<something|another_possible_one|a_third>`) with "<"
        arg_subcmds = ''
        # For each element in the array
        for i in command_signatures:
            # Remove all backticks (`) and replace the occuring value of tostrip with nothing. Add it to the string as well as a |
            arg_subcmds += f"{i.replace(tostrip, '').strip('`')}|"
        # Remove the last "|" and add the last ">"
        arg_subcmds = f'<{arg_subcmds[:-1]}>'
         print(arg_subcmds)
        # If there were no subcommands
        if arg_subcmds == '<>':
            arg_subcmds = None
        else:
            # Surround it with backticks for the codeblock in Discord
            arg_subcmds = f'`{arg_subcmds}`'
        # Checks if the group has aliases
        if len(group.aliases) == 0:
            aliases = None
        else:
            aliases = []
            # For each element in group.aliases
            for i in group.aliases:
                # Adds all of the aliases to a new list with backticks around each individual element
                aliases.append(f'`{i}`')
             # Joins the array with ", " between each element
            aliases = ', '.join(aliases)
        # Embed generation
        embed = discord.Embed(title=f'Help for {group.name}', description=f'Displaying help for {group}.\n`<>` marks required parameters.\n`[]` marks optional parameters.', color=random.choice(embedcolours))
        embed.add_field(name=f'Description', value=group.description, inline=False)
        embed.add_field(name=f'Aliases', value=aliases, inline=False)
        # Different depending on if there were subcommands
        if arg_subcmds:
           embed.add_field(name=f'Usage', value=f'`_{group.name}` {arg_subcmds}', inline=False)
        else:
           embed.add_field(name=f'Usage', value=f'`_{group}`', inline=False)
        embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
        # Send as a reply
        await self.context.reply(embed=embed)

    
    # Used when someone does "_help <command name>"
    async def send_command_help(self, command):
        # If the user has access to use the command
        if await self.filter_commands([command], sort=True):
            # Embed generation
            embed = discord.Embed(title=f"Help for {command.name}", description=f'Displaying help for {command.name}.\n`<>` marks required parameters.\n`[]` marks optional parameters.', color=random.choice(embedcolours))
            embed.add_field(name='Description', value=command.description, inline=False)
            # For aliases, same as above
            if len(command.aliases) == 0:
                aliases = None
            else:
                aliases = []
                for i in range(len(command.aliases)):
                    aliases.append(f'`{command.aliases[i]}`')
                    aliases = ', '.join(aliases)
            embed.add_field(name='Aliases', value=aliases, inline=False)
            embed.add_field(name='Usage', value=self.get_command_signature(command), inline=False)
            embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
            # Send embed as a reply
            await self.context.reply(embed=embed)
        # If user doesn't have permission to use command
        else:
            await self.get_destination().send(f'No command called "{command.name}" found.')

    # If an error occurs in the help message
    async def on_help_command_error(self, ctx, error):
        # If it's a bad argument
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            embed.set_author(name='Help', icon_url=self.context.author.avatar_url)
            await ctx.reply(embed=embed)
        # Otherwise, raise the error
        else:
            raise error

# Create the cog for the help command to be in the bot
class Help(commands.Cog, name='Help'):
    """Get help with commands!"""
    def __init__(self, client):
        self.client = client

       # Setting the cog for the help
        help_command = MyHelp(command_attrs=attributes)
        help_command.cog = self # Instance of YourCog class
        self.client.help_command = help_command


# Allows cog to be loaded
def setup(client):
    client.add_cog(Help(client))
