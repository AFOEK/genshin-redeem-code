# https://realpython.com/how-to-make-a-discord-bot-python/
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>>',intents=intents)
msg = []

@bot.event
async def on_connect():
    print(f'{bot.user.name} has connected to Discord!') #just for debugging
    
@bot.event
async def on_ready():
    global msg
    print(f'{bot.user.name} is starting to scrape message from UID channel')
    ch =  bot.get_channel(821006600424652840)
    msg = await ch.history(limit=50).flatten()
    print(f'{bot.user.name} success fully scape message from UID Channel')
    print(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Missing Argument ! <:jean_question:833542806001025056>")

@bot.command(name='redeem', help="Usage: !redeem 'uid' 'redeem_code' 'server_region'. If server region is ommited it will asume asia server")
async def redeem(ctx,uid,redeem_code,srv_reg: Optional[str] = None):
    print(f'{bot.user.name} getting input from discord client')
    redeem_code = redeem_code.upper()   #This will make redeem code become capitalized
    res=f'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'    #redeem link

    if(uid.isnumeric() and len(uid)!=9):    #check if "UID" is UID
        res = f'Invalid UID !'  #Error message

    if(srv_reg is None):
        srv_reg = 'asia'
        res = f'Since no server region get specified, it will assume asia region\nhttps://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'
    print (uid,redeem_code,srv_reg)
    await ctx.send(res)

bot.run(TOKEN)