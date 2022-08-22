# https://realpython.com/how-to-make-a-discord-bot-python/
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents.all()
intents.member = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!') #just for debugging

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