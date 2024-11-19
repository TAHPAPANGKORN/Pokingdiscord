import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from myserver import server_on
import os

bot = commands.Bot(command_prefix="\\", intents=discord.Intents.all(),help_command=None)

TOKEN = os.environ.get('token')


status = ['Just Find A AFK Member','Move AKF Member']
stopLoop = None


#--------- check ---------
@bot.event
async def on_ready():
    global text
    text = "Now online!!"
    print(text)
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(status[0])) #bot status when start
    synced = await bot.tree.sync()
    print(f'{len(synced)} command(s)')

@bot.command(aliases=['ready','start'])
async def _ready(ctx):
    await ctx.send("online")
#--------- end check ---------
    

#--------- help ---------
def emmbedShow():
    emmbed = discord.Embed(   
        title='Help Me! - Bot Commands',
        description='**Commands with "\\\\" prefix :**\n\help\n\stop\n\n'
                    '**Slash Commands with "/" prefix :**\n/help\n/move\n/stop\n/tah',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    return emmbed

@bot.command(aliases=['help','help_me','hp'])
async def _help(ctx):
    emmbed = emmbedShow()
    await ctx.channel.send(embed=emmbed)


@bot.tree.command(name='help', description='Need help')
async def helpCommand(ctx):
    emmbed = emmbedShow()
    await ctx.channel.send(embed=emmbed)
#--------- end help ---------


#--------- move ---------
@bot.tree.command(name='move', description='Move and create poking room')
async def wakeMove(ctx, member: discord.Member, number: int):
    global stopLoop, nameMember
    nameMember = member.name
    if number <= 0:
        await ctx.response.send_message("โปรดระบุจำนวนรอบที่มากกว่า 0!")
        return
    if not member.voice:
        await ctx.response.send_message(f"{member.mention} ไม่ได้อยู่ใน Voice Channel!")
        return
    original_channel = member.voice.channel
    try:
        await ctx.channel.send(f"{ctx.user.name} move {member.mention}")
        channel1 = await ctx.guild.create_voice_channel("ปลุก 1")
        channel2 = await ctx.guild.create_voice_channel("ปลุก 2")

        for attempt in range(number):
            if not stopLoop:
                await asyncio.gather( # .gather(variable, variable) 
                    member.send(f"{ctx.user.mention} กำลังเรียกคุณครั้งที่ {attempt+1}"),
                    member.move_to(channel1)
                )
                await asyncio.sleep(1)  # Wait for 0.5 seconds
                await member.move_to(channel2)
                  
        # Move back to the original channel
        stopLoop = False
        await member.move_to(original_channel)
        await member.send(f"{member.mention} เราพยายามปลุกคุณแล้ว!")
    except Exception as e:
        await ctx.response.send_message(f"เกิดข้อผิดพลาด: {e}")
    finally:
        # Clean up channels
        stopLoop = None
        await channel1.delete()
        await channel2.delete()
#--------- end move ---------


#--------- call tah ---------
@bot.tree.command(name='tah', description='Call cheetah to your room')
async def callTah(ctx: discord.Interaction):
    tahId = 577053817674268673  # User ID as an integer
    tahMember = ctx.guild.get_member(tahId)  # Fetch the Member object

    if tahMember is None:
        await ctx.response.send_message("User with the specified ID is not in this server.")
        return

    tah = tahMember.mention  # Discord name

    if ctx.user.voice and ctx.user.voice.channel:
        targetChannel = ctx.user.voice.channel
    else:
        await ctx.response.send_message("You must be in a voice channel to call someone.")
        return

    if tahMember.voice and tahMember.voice.channel == targetChannel:
        await ctx.response.send_message(f"{tah} is already in your room.")
        return

    if tahMember.voice:
        try:
            await tahMember.move_to(targetChannel)
            await ctx.response.send_message(f"Called {tah} to room {targetChannel.name}.")
        except Exception as e:
            await ctx.response.send_message(f"Failed to move {tah}: {str(e)}")
    else:
        await ctx.response.send_message(f"{tah} is not currently in a voice channel.")
#--------- end call tah ---------


#--------- stop ---------
@bot.command()
async def stop(ctx):
    global stopLoop
    stopLoop = True
    await ctx.channel.send(f"{ctx.user.name} stop {nameMember}")
    await ctx.user.send(f'คุณหยุดการปลุก')

@bot.tree.command(name='stop', description='Stop Move Some Member')
async def stop(ctx):
    global stopLoop
    stopLoop = True
    await ctx.channel.send(f"{ctx.user.name} stop {nameMember}")
    await ctx.user.send(f'คุณหยุดการปลุก')
#--------- end stop ---------


  
server_on()
bot.run(TOKEN)



