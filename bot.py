import os
import time
import discord
import asyncio
import RPi.GPIO as GPIO
from discord.ext import commands

bot = discord.Client()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/22-000000573444/w1_slave'

TOKEN = 'NTQ3MzExNDgyODk2MTIxODU3.D01E-g.U5UwWct9U_JUaw5Hc35R-3GN0-M'

description = '''Tempbot22 in Python'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
        temp_f = temp_c * 9.0/5.0+32.0
        return temp_c, temp_f





@bot.command()
async def temp():
    await bot.say(read_temp())


@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)
    

async def aa():
    await bot.wait_until_ready()
    channel = discord.Object(id='547310311397523461')
        
    while not bot.is_closed:
        if GPIO.input(10) == GPIO.HIGH:
            await bot.send_message(channel, read_temp())
            await asyncio.sleep(1)
        
bot.loop.create_task(aa())
bot.run(TOKEN)
