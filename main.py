import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from help_cog import help_cog
from music_cog import music_cog

load_dotenv()  # Load environment variables from .env file

token = os.getenv('TOKEN')
if token is None:
    raise ValueError("No TOKEN found in environment variables")

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='-', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def setup():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))

async def main():
    await setup()
    await bot.start(token)

import asyncio
asyncio.run(main())