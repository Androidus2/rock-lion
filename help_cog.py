import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'], help='Show this message')
    async def help(self, ctx):
        """
        Show the help message
        """
        help_message = '```'
        for command in self.bot.commands:
            help_message += f'{command.name}: {command.help}\n'
        help_message += '```'
        await ctx.send(help_message)