# https://realpython.com/how-to-make-a-discord-bot-python/  based by
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
    global df_chat  #make dataframe become global so it can be access by other function
    print(f'{bot.user.name} is starting to scrape message from UID channel')    #for just debugging
    ch =  bot.get_channel(821006600424652840)   #Channel id of UID Channel
    async for msg in ch.history(limit=75,oldest_first=True):    #Get all message from UID Channel
        df_chat = df_chat.append({  # it's append data into dataframe
            'dc_usr_id':msg.author.id,
            'dc_usrname':msg.author.name,
            'msg_content': msg.content,
        }, ignore_index=True)
    
    df_chat['msg_content'].replace(to_replace=r'\D+', value='', regex=True, inplace=True)   #Sanitize all UID
    #This brute force sanitize, my brain can't create sophisticated regex, awk, or grep equivalent gibberish. Since I pull DC data as it and ordered it
    #from oldest to new (from top to bottom)
    df_chat.loc[2,'msg_content'] = '817082429'
    df_chat.loc[20,'msg_content'] = '807802802'
    df_chat.loc[23,'msg_content'] = '813693892'
    df_chat.loc[2.5] = '629284960112476160', 'lacie', '813746049'
    df_chat.loc[23.5] = '516850719609978883', 'Lost', '817011863'
    df_chat.drop([6],axis=0,inplace=True)
    df_chat = df_chat.sort_index().reset_index(drop=True)
    df_chat.insert(3, "primary_account", True)
    df_chat.loc[2,'primary_account'] = False
    df_chat.loc[20,'primary_account'] = False
    print(f'{bot.user.name} success fully scrape message from UID Channel') #Just for debugging
    print(df_chat.head(70)) #Just for debugging

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):  #Handling Error
        await ctx.send("Missing Argument ! <:jean_question:833542806001025056>")    #Post into Text Channel if something go wrong
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("Bad Argument ! <:PaimonAngry:833542865690558515>")

@bot.command(name='redeem', usage="Usage: >>redeem 'redeem_code*' 'uid[Optional]' 'server_region[Optional]'", help="It will make a link for redeeming genshin impact code. If server region is ommited it will asume asia server")
async def redeem(ctx,redeem_code,uid:Optional[str] = None,srv_reg: Optional[str] = None):
    print(f'{bot.user.name} getting input from discord client') #Just for debugging
    redeem_code = redeem_code.upper()   #This will make redeem code become capitalized
    if(uid.isnumeric() and len(uid)==9 and uid != None):    #check if "UID" are given
        res=f'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'    #redeem link
    elif(uid == None):  #check if "UID" are not given
        auth = ctx.author.id    #get the message author
        uid = df_chat.query('dc_usr_id == @auth and primary_account == True')['msg_content']
        res=f'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'    #redeem link
    else:
        raise discord.ext.commands.errors.BadArgument

    if(srv_reg is None):
        srv_reg = 'asia'
        res = f'Since no server region get specified, it will assume asia region\nhttps://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'
    print (uid,redeem_code,srv_reg) #Just for debugging
    await ctx.send(res) #send back response

bot.run(TOKEN)