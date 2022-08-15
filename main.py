# https://realpython.com/how-to-make-a-discord-bot-python/
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='>')
@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected into discord'
    )

async def on_message(message):
    if message.author == bot.user:
        return

async def on_error(event, *args, **kwargs):
    with open('err.log','a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')

bot.run(TOKEN)