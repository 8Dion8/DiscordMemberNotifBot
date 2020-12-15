import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import steammarket as sm
from numpy import transpose

print("\n\n\n\n\n\n\n\n")

bot = commands.Bot(command_prefix='$')

asleep = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print('Бот онлайн епт')
    channel = bot.get_channel(775400125144498186)
    await channel.send('Бот онлайн епт')

@bot.command()
async def help_me(ctx):
    if not asleep:
        message = '''Список комманд:
        
        ```
        Название - использование - функция

        map - $map режим число - печатает число карт, в зависимости режима - normal или stupid

        case - $case "name" - печатает цену предмета кс с именем name

        die - $die - заставляет бота умереть в страшных муках

        stfu - $stfu - для особо одаренных

        cum - $cum - если нечего делать
        ```'''
        await ctx.send(message)

@bot.command()
async def map(ctx, mode, amount):
    if not asleep:
        await ctx.send('Выбираем карту...')
        if mode == 'normal':
            maps = ['Inferno','Lake','Nuke']
        elif mode == 'stupid':
            maps = ['Cobblestone','Inferno','Lake','Nuke','Overpass','Rialto','Shortdust','Train','Vertigo']
        try:
            chosen = random.sample(maps, int(amount))
            formatted = "Карты: "+", ".join(chosen)+"\nудачи хуле ахахахахах"
            await ctx.send(formatted)
        except:
            await ctx.send("Ты где-т накосячил. Либо режим шизоидный, либо карт дохуя хочешь. Валв столько не делает своей ленивой жопой))")
@bot.command()
async def case(ctx, name):
    if not asleep:
        item = sm.get_csgo_item(name, currency="RUB")
        await ctx.send(item['volume'] + ' предметов на продажу, самый дешевый стоит ' + item['lowest_price'])


@bot.command()
async def sleep(ctx):
    global asleep
    if not asleep:
        await ctx.send('Лан, я пошел поспать))')
        
        asleep = True
    
@bot.command()
async def wake_up(ctx):
    global asleep
    if asleep:
        await ctx.send('Да не сплю я мам')
        asleep = False
    else:
        await ctx.send('Лол я не сплю')
        

@bot.command()
async def online(ctx):
    global asleep
    if not asleep:
        online_members = []
        offline_members = []
        ctx.send(ctx.guild.members)
        async for user in ctx.guild.fetch_members(limit=None):
            if user.status == discord.Status.offline:
                offline_members.append(user.name + '#' + user.discriminator)
            else:
                online_members.append(user.name + '#' + user.discriminator)

        print(online_members,offline_members)
        await ctx.send(f'Я вижу {len(online_members)} додика без социальной жизни и {len(offline_members)} человека которые спят')

        
def check(author):
    def inner_check(message):
        return message.author == author and message.content in '0123456789'
    return inner_check

@bot.command()
async def rps(ctx, member):
    await ctx.send(member + ", " + ctx.author.name + " вызывает вас на дуэль в крестики нолики!")

    game_running = True
    board = [[0,1,2],[3,4,5],[6,7,8]]

    while game_running:
        await ctx.send(member + ", " + " Выберете цифру, куда будете ставить крестик:")

        message = '```\n'
        for arr in board:
            message +=  "|".join(str(j) for j in arr) + "\n"
        message += "```"
        await ctx.send(message)


        got_input = False
        while not got_input:
            message = await bot.wait_for('message', check=check(ctx.author))
            print(message)
            while True:
                try:
                    print(type(message.content),message.content)
                    place = int(message.content)
                    got_input = True
                    if board[place//3][place%3] != place:
                        
                        raise Exception
                    else:
                        board[place//3][place%3] = 'X'
                        print("got input")
                        got_input = True
                        break
                except:
                    await ctx.send('Введи норм цифру')

        message = '```\n'
        for arr in board:
            message +=  "|".join(str(j) for j in arr) + "\n"
        message += "```"
        await ctx.send(message)

        for i in board:
            if "".join(i) == "".join(['X','X','X']) or "".join(i) == "".join(['O','O','O']):
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                break
        for i in transpose(board):
            if "".join(i) == "".join(['X','X','X']) or "".join(i) == "".join(['O','O','O']):
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                break
        if board[0][0] == board[1][1] == board[2][2]:
            await ctx.send(board[0][0] + ' выиграл!')
            game_running = False
            break
        elif board[0][2] == board[1][1] == board[2][0]:
            await ctx.send(board[0][2] + ' выиграл!')
            game_running = False
            break

        got_input = False
        while not got_input:
            message = await bot.wait_for('message', check=check(ctx.author))
            print(message)
            while True:
                try:
                    print(type(message.content),message.content)
                    place = int(message.content)
                    got_input = True
                    if board[place//3][place%3] != place:
                        
                        raise Exception
                    else:
                        board[place//3][place%3] = 'X'
                        print("got input")
                        got_input = True
                        break
                except:
                    await ctx.send('Введи норм цифру')
        
        for i in board:
            if "".join(i) == "".join(['X','X','X']) or "".join(i) == "".join(['O','O','O']):
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                break
        for i in transpose(board):
            if "".join(i) == "".join(['X','X','X']) or "".join(i) == "".join(['O','O','O']):
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                break
        if board[0][0] == board[1][1] == board[2][2]:
            await ctx.send(board[0][0] + ' выиграл!')
            game_running = False
            break
        elif board[0][2] == board[1][1] == board[2][0]:
            await ctx.send(board[0][2] + ' выиграл!')
            game_running = False
            break
        

        

@bot.command()
async def stfu(ctx):
    global asleep
    if not asleep:
        await ctx.send('А нахуй не пойдешь? Будешь выебываться - @Главбух тебя забанит')

@bot.command()
async def cum(ctx):
    global asleep
    if not asleep:
        await ctx.send(file=discord.File('maxresdefault.jpg'))

bot.run(TOKEN)