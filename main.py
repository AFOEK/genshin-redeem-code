# https://realpython.com/how-to-make-a-discord-bot-python/
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional
import re
import numpy
import pandas as pd

load_dotenv()   #Load neccessary env
TOKEN = os.getenv('DISCORD_TOKEN')  #Load token into variable
intents = discord.Intents.all() #Set intents
bot = commands.Bot(command_prefix='>>',intents=intents) #Bot init
df_chat =  pd.DataFrame(columns=['dc_usr_id','dc_usrname','msg_content'])   #Creating dataframe, it's wiser to make dataframe than expost it into hard csv

@bot.event
async def on_connect():
    print(f'{bot.user.name} has connected to Discord!') #just for debugging

@bot.event
async def on_ready():
    global df_chat
    print(f'{bot.user.name} is starting to scrape message from UID channel')    #for just debugging
    ch =  bot.get_channel(821006600424652840)   #UID Channel
    async for msg in ch.history(limit=75,oldest_first=True):
        df_chat = df_chat.append({
            'dc_usr_id':msg.author.id,
            'dc_usrname':msg.author.name,
            'msg_content':msg.content
        }, ignore_index=True)
    print(f'{bot.user.name} success fully scrape message from UID Channel') #Just for debugging
    print(df_chat.head(70))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):  #Handling Error
        await ctx.send("Missing Argument ! <:jean_question:833542806001025056>")

@bot.command(name='redeem', usage="Usage: >>redeem 'uid*' 'redeem_code*' 'server_region[Optional]'", help="It will make a link for redeeming genshin impact code. If server region is ommited it will asume asia server")
async def redeem(ctx,uid,redeem_code,srv_reg: Optional[str] = None):
    print(f'{bot.user.name} getting input from discord client') #Just for debugging
    redeem_code = redeem_code.upper()   #This will make redeem code become capitalized
    res=f'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'    #redeem link

    if(uid.isnumeric() and len(uid)!=9):    #check if "UID" is UID
        res = f'Invalid UID !'  #Error message

    if(srv_reg is None):
        srv_reg = 'asia'
        res = f'Since no server region get specified, it will assume asia region\nhttps://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'
    print (uid,redeem_code,srv_reg) #Just for debugging
    await ctx.send(res)

bot.run(TOKEN)