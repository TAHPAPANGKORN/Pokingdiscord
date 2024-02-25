import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from myserver import server_on
import os

bot = commands.Bot(command_prefix="\\", intents=discord.Intents.all(),help_command=None)

TOKEN = os.environ.get('token')



status = ['Just Find A AFK Member','Move AKF Member']
stop_loop = False

@bot.event
async def on_ready():
    global text
    text = "Now online!!"
    print(text)
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(status[0])) #bot status when start
    synced = await bot.tree.sync()
    print(f'{len(synced)} command(s)')
    # channel = bot.get_channel(682225304991039573)
    # await channel.send(text)
    
  


@bot.command(aliases=['ready','start'])
async def _ready(ctx):
    await ctx.send("online")
    
    
@bot.command(aliases=['help','helpme','hp'])
async def _help(ctx):
    emmbed = discord.Embed(
        title='Help Me! - Bot Commands',
        description='**Commands with "\\\\" prefix :**\n\help\n\move @name Set number of times\n\stop\n\n'
                    '**Slash Commands with "/" prefix :**\n/move\n/stop\n/help',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    await ctx.channel.send(embed=emmbed)



@bot.tree.command(name='help', description='Need help')
async def helpCommand(ctx):
    emmbed = discord.Embed(
        title='Help Me! - Bot Commands',
        description='**Commands with "\\\\" prefix :**\n\help\n\move @name Set number of times\n\stop\n\n'
                    '**Slash Commands with "/" prefix :**\n/move\n/stop\n/help',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    await ctx.response.send_message(embed=emmbed)



@bot.tree.command(name='move', description='Move Some Member')
async def moveCommand(ctx, member:discord.Member,number : int):
    channel1 = bot.get_channel(1208770282245070991)
    channel2 = bot.get_channel(1208776120582012978)
    original_channel = member.voice.channel
    global stop_loop
    for i in range(int(number)) :    
        if stop_loop == True:
            await ctx.channel.send("stop")
            await member.move_to(original_channel)
            stop_loop = False  
            break
        await member.move_to(channel1)
        await asyncio.sleep(0.5)
        await member.move_to(channel2)
        await bot.change_presence(activity=discord.Game(status[1])) #bot status when move some person
        print(i+1,end=" ")
        
    await member.move_to(original_channel)
    await bot.change_presence(activity=discord.Game(status[0]))


@bot.command()
async def move(ctx, member:discord.Member,number) :
    channel1 = bot.get_channel(1208770282245070991)
    channel2 = bot.get_channel(1208776120582012978)
    original_channel = member.voice.channel
    global stop_loop
    for i in range(int(number)) :    
        if stop_loop:
            await ctx.send("stop")
            await member.move_to(original_channel)
            stop_loop = False  
            break
        await member.move_to(channel1)
        await asyncio.sleep(0.5)
        await member.move_to(channel2)
        await bot.change_presence(activity=discord.Game(status[1])) #bot status when move some person
        print(i+1,end=" ")
        
    await member.move_to(original_channel)
    await bot.change_presence(activity=discord.Game(status[0]))


@bot.command()
async def stop(ctx):
    global stop_loop
    stop_loop = True

@bot.tree.command(name='stop', description='Stop Move Some Member')
async def stop(ctx):
    global stop_loop
    stop_loop = True


  
server_on()
bot.run(TOKEN)



