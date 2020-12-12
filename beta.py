import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='$')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print('Бот онлайн епт')
    channel = bot.get_channel(775400125144498186)
    await channel.send('Бот онлайн епт')


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
    await channel.send('А нахуй не пойдешь? Будешь выебываться - @Dion тебя забанит')
@bot.command()
async def cum(ctx):
    channel = bot.get_channel(775400125144498186)
    await channel.send(file=discord.File('maxresdefault.jpg'))

bot.run(TOKEN)