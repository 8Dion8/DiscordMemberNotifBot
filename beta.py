import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import steammarket as sm

bot = commands.Bot(command_prefix='$')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print('Бот онлайн епт')
    channel = bot.get_channel(775400125144498186)
    await channel.send('Бот онлайн епт')

@bot.command()
async def map(ctx, mode, amount):
    channel = bot.get_channel(775400125144498186)
    await channel.send('Выбираем карту...')
    if mode == 'normal':
        maps = ['Inferno','Lake','Nuke']
    elif mode == 'stupid':
        maps = ['Cobblestone','Inferno','Lake','Nuke','Overpass','Rialto','Shortdust','Train','Vertigo']
    try:
        chosen = random.sample(maps, int(amount))
        formatted = "Карты: "+", ".join(chosen)+"\nудачи хуле ахахахахах"
        await channel.send(formatted)
    except:
        await channel.send("Ты где-т накосячил. Либо режим шизоидный, либо карт дохуя хочешь. Валв столько не делает своей ленивой жопой))")
@bot.command()
async def case(ctx, name):
    item = sm.get_csgo_item(name, currency="RUB")
    channel = bot.get_channel(775400125144498186)
    await channel.send(item['volume'] + ' предметов на продажу, самый дешевый стоит ' + item['lowest_price'])

@bot.command()
async def die(ctx):
    channel = bot.get_channel(775400125144498186)
    await channel.send('Чо так агрессивно то. Лан, я пошел))')
    sys.exit()

@bot.command()
async def online(ctx):
    online_members = []
    offline_members = []
    channel = bot.get_channel(775400125144498186)
    channel.send(ctx.guild.members)
    async for user in ctx.guild.fetch_members(limit=None):
        if user.status == discord.Status.offline:
            offline_members.append(user.name + '#' + user.discriminator)
        else:
            online_members.append(user.name + '#' + user.discriminator)

    print(online_members,offline_members)
    await channel.send(f'Я вижу {len(online_members)} додика без социальной жизни и {len(offline_members)} человека которые спят')


@bot.command()
async def stfu(ctx):
    channel = bot.get_channel(775400125144498186)
    await channel.send('А нахуй не пойдешь? Будешь выебываться - @Главбух тебя забанит')

@bot.command()
async def cum(ctx):
    channel = bot.get_channel(775400125144498186)
    await channel.send(file=discord.File('maxresdefault.jpg'))

bot.run(TOKEN)