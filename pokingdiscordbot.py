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
    text = [["/help", ": Provides help or detailed information about available commands."],
            ["/move", ": Used to wake up friends."],
            ["/stop", ": Stops or cancels the current process or action of the bot."],
            ["/link", ": Generates or shares a specific link or connection."]]
    
    emmbed = discord.Embed(
        title='Help Me! - Bot Commands',
        description=f'**Commands with "\\\\" prefix :**\n**\help**{text[0][1]}\n**\stop**{text[2][1]}\n\n'
                    f'**Recommend** ↓\n'
                    f'**Slash Commands with "/" prefix : **\n**{text[0][0]}**{text[0][1]}\n**{text[1][0]}**{text[1][1]}\n**{text[2][0]}**{text[2][1]}\n**{text[3][0]}**{text[3][1]}\n\n'
                    '**⚠️ Important :\n ถ้าคนที่ Poke ไม่ได้เปิดการแจ้งเตือนจะทำงานได้ไม่เต็มประสิทธิภาพ**\n',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    return emmbed

@bot.command(aliases=['help','help_me','hp'])
async def _help(ctx):
    emmbed = emmbedShow()
    await ctx.channel.send(embed=emmbed)


@bot.tree.command(name="help", description="Show help information")
async def _help(ctx: discord.Interaction):
    await ctx.response.defer(ephemeral=True)
    emmbed = emmbedShow()  
    await ctx.followup.send(embed=emmbed, ephemeral=True)
#--------- end help ---------

#--------- link ---------
@bot.tree.command(name='invite', description='Get Link To Invite')
async def sendLink(ctx: discord.Interaction):
    await ctx.response.defer(ephemeral=True)
    # Create the embed
    emmbed = discord.Embed(
        title='Link for invite this bot',
        description='Click the button below to invite bot.',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    # Create a button
    view = discord.ui.View()
    button1 = discord.ui.Button(
        label="Invite bot", 
        style=discord.ButtonStyle.link, 
        url='https://discord.com/oauth2/authorize?client_id=1208764608727359601&permissions=16778256&integration_type=0&scope=bot'
    )
    
    async def button2Callback(interaction: discord.Interaction):
        # Send a follow-up message when button2 is clicked
        await interaction.response.send_message(
            "Here is the invite link for the bot: https://discord.com/oauth2/authorize?client_id=1208764608727359601&permissions=16778256&integration_type=0&scope=bot", 
            ephemeral=True
        )
    button2 = discord.ui.Button(
        label="Invite link", 
        style=discord.ButtonStyle.primary
    )
    button2.callback = button2Callback

    # Add buttons to the view
    view.add_item(button1)
    view.add_item(button2)
    await ctx.followup.send(embed=emmbed, view=view, ephemeral=True)
#--------- end link ---------


#--------- move ---------
@bot.tree.command(name='move', description='Move and create poking room')
async def wakeMove(ctx: discord.Interaction, member: discord.Member, number: int):
    global stopLoop, nameMember
    nameMember = member.name

    # Acknowledge the interaction immediately
    await ctx.response.defer(ephemeral=True)
   
    if number <= 0:
        await ctx.followup.send("Please specify the number of rounds greater than 0!")
        return
    if not member.voice:
        await ctx.followup.send(f"{member.mention} Not In Voice Channel!")
        return

    originalChannel = member.voice.channel
    try:
        await ctx.followup.send(f"{ctx.user.name} move {member.mention} {number} times")  # Initial response
        channel1 = await ctx.guild.create_voice_channel("Poke room 1")
        channel2 = await ctx.guild.create_voice_channel("Poke room 2")

        for attempt in range(number):
            if not stopLoop:
                await asyncio.gather(
                    member.send(f"{ctx.user.mention} Calling you for the {attempt+1} time"),
                    member.move_to(channel1)
                )
                await asyncio.sleep(1)  # Wait for 1 second
                await member.move_to(channel2)

        # Move back to the original channel
        stopLoop = False
        await member.move_to(originalChannel)
        await member.send(f"{member.mention} We tried to wake you up!")
    except Exception as e:
        await ctx.followup.send(f"Error: {e}")
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
    await ctx.response.defer(ephemeral=True)
    # Stop the loop
    stopLoop = True
    if nameMember:
        await ctx.followup.send(f'You stop poke {nameMember}.', ephemeral=True)
    else:
        await ctx.followup.send('There is no trigger currently operating.', ephemeral=True)

@bot.tree.command(name='stop', description='Stop Move Some Member')
async def stop(ctx: discord.Interaction):
    global stopLoop
    await ctx.response.defer(ephemeral=True)
    # Stop the loop
    stopLoop = True
    if nameMember:
        await ctx.followup.send(f'You stop poke {nameMember}.', ephemeral=True)
    else:
        await ctx.followup.send('There is no trigger currently operating.', ephemeral=True)
#--------- end stop ---------


  
server_on()
bot.run(TOKEN)



