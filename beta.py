import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import steammarket as sm
from numpy import transpose
from gen_board import gen_board
import json
import matplotlib.pyplot as plt

#change plot theme to match discord
plt.rcParams.update({
    "figure.facecolor": "#36393E",
    "figure.edgecolor": "#36393E",
    "savefig.facecolor": "#36393E",
    "savefig.edgecolor": "#36393E",
    "text.color": "white"
})

print("\n\n\n\n\n\n\n\n")


#initialise client
bot = commands.Bot(command_prefix='$')

asleep = False

#get secret discord token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


#send a message when bot goes online
@bot.event
async def on_ready():
    print('Бот онлайн епт')
    channel = bot.get_channel(775400125144498186)
    await channel.send('Бот онлайн епт')
    
#whenever a message is sent to any server, then update the json stats before executing commands
@bot.event
async def on_message(message):
    #load json
    with open("/Users/glebsvarcer/Documents/DiscordMemberNotifBot/data.json","r") as f:
        data = json.load(f)

    #update message count
    data["users"][str(message.author.id)]["message_count"][str(message.channel.id)]["count"] += 1

    #save json
    with open("/Users/glebsvarcer/Documents/DiscordMemberNotifBot/data.json","w") as f:
        json.dump(data,f)

    #execute commands if any in the message
    await bot.process_commands(message)

#resets the json data
async def create_json():
    #get bot_testing channel
    channel = bot.get_channel(775400125144498186)


    data = {
        "users":{

        }
    }

    #create the base json structure for every user
    async for member in channel.guild.fetch_members(limit=None):

        data["users"][str(member.id)] = {}
        data["users"][str(member.id)]["name"] = member.name
        data["users"][str(member.id)]["discriminator"] = member.discriminator
        data["users"][str(member.id)]["message_count"] = {}

        print(data)

        for guild in bot.guilds:
            for channel in guild.text_channels:
                data["users"][str(member.id)]["message_count"][str(channel.id)] = {
                    "name":channel.name,
                    "count":0
                }

    print(data)

    #update each user's data based on the message history
    for guild in bot.guilds:
        for channel in guild.text_channels:
            #get message history
            messages = await channel.history(limit=200).flatten()
            for message in messages:
                #update the message count
                data["users"][str(message.author.id)]["message_count"][str(channel.id)]["count"] += 1

    print(json.dumps(data,indent=4))

    #save data
    with open("/Users/glebsvarcer/Documents/DiscordMemberNotifBot/data.json","w") as f:
        json.dump(data,f)


#define a help command
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


#define a command that picks CSGO Wingman maps at random
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


#define a command that sends Steam Community Market prices for a given item
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

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
        
def check(author):
    def inner_check(message):
        print(author)
        return str(message.author.id) == author[3:len(author)-1] and message.content[0] in '0123456789'
    return inner_check

@bot.command()
async def ttt(ctx, member, size):
    size = int(size)
    if size < 1 or size > 10:
        await ctx.send("Выбери нормальный размер")
        return
    await ctx.send(member + ", " + ctx.author.name + " вызывает вас на дуэль в крестики нолики!")

    game_running = True
    board = gen_board(size)

    while game_running:
        await ctx.send(member + ", " + " Выберете цифру, куда будете ставить крестик:")

        message = '```python\n'
        for arr in board:
            message +=  "|".join(str(j)+" " if len(str(j))==1 else str(j) for j in arr) + "\n"
        message += "```"
        await ctx.send(message)


        got_input = False
        while not got_input:
            message = await bot.wait_for('message', check=check(member))
            print(message)
            while True:
                try:
                    print(type(message.content),message.content)
                    place = int(message.content)
                    got_input = True
                    if board[place//size][place%size] != place:
                        raise Exception
                    else:
                        board[place//size][place%size] = 'X'
                        print("got input")
                        got_input = True
                        break
                except:
                    await ctx.send('Введи норм цифру')

        message = '```python\n'
        for arr in board:
            message +=  "|".join(str(j)+" " if len(str(j))==1 else str(j) for j in arr) + "\n"
        message += "```"
        await ctx.send(message)

        for i in board:
            if "".join(str(r) for r in i) == 'X'*size or "".join(str(r) for r in i) == 'O'*size:
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                return
        for i in transpose(board):
            if "".join(str(r) for r in i) == 'X'*size or "".join(str(r) for r in i) == 'O'*size:
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                return
        args = []
        for i in range(size):
            args.append(str(board[i][i]))
        if "".join(args) == 'O'*size or "".join(args) == 'X'*size:
            await ctx.send(board[0][0] + ' выиграл!')
            game_running = False
            return
        args = []
        for i in range(size):
            print(i,size)
            args.append(str(board[i][size-i-1]))
        if "".join(args) == 'O'*size or "".join(args) == 'X'*size:
            await ctx.send(board[0][2] + ' выиграл!')
            game_running = False
            return
        else: 
            str_board = "".join(["".join(str(p) for p in y) for y in board])
            print(str_board)
            if not hasNumbers(str_board):
                await ctx.send("Ничья!")
                game_running = False
                return

        await ctx.send("<@!" + str(ctx.author.id) + "> , " + " Выберете цифру, куда будете ставить нолик:")

        got_input = False
        while not got_input:
            message = await bot.wait_for('message', check=check("<@!" + str(ctx.author.id) + ">"))
            print(message)
            while True:
                try:
                    print(type(message.content),message.content)
                    place = int(message.content)
                    got_input = True
                    if board[place//size][place%size] != place:
                        
                        raise Exception
                    else:
                        board[place//size][place%size] = 'O'
                        print("got input")
                        got_input = True
                        break
                except:
                    await ctx.send('Введи норм цифру')
        
        for i in board:
            if "".join(str(r) for r in i) == 'X'*size or "".join(str(r) for r in i) == 'O'*size:
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                return
        for i in transpose(board):
            if "".join(str(r) for r in i) == 'X'*size or "".join(str(r) for r in i) == 'O'*size:
                await ctx.send(i[0] + ' выиграл!')
                game_running = False
                return
        args = []
        for i in range(size):
            args.append(str(board[i][i]))
        if "".join(args) == 'O'*size or "".join(args) == 'X'*size:
            await ctx.send(board[0][0] + ' выиграл!')
            game_running = False
            return
        args = []
        for i in range(size):
            args.append(str(board[i][size-i-1]))
        if "".join(args) == 'O'*size or "".join(args) == 'X'*size:
            await ctx.send(board[0][2] + ' выиграл!')
            game_running = False
            return
        else: 
            str_board = "".join(["".join(str(p) for p in y) for y in board])
            print(str_board)
            if not hasNumbers(str_board):
                await ctx.send("Ничья!")
                game_running = False
                return

        
@bot.command()
async def shutdown(ctx):
    if ctx.message.author.id == 420905534535892992:
        print("shutdown")
        try:
            await bot.logout()
        except:
            print("EnvironmentError")
            bot.clear()
    else:
        await ctx.send("У вас нет прав на эту комманду (лох)")

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

@bot.command()
async def reset_data(ctx):
    if ctx.message.author.id == 420905534535892992:
        await create_json()
        await ctx.send("Данные созданы заново.")
    else:
        ctx.send("Хорошая попытка но не, у тя прав нет")
    
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct

@bot.command()
async def stats(ctx, target, name):
    if target == "user":
        user_id = name[3:len(name)-1]
        with open("/Users/glebsvarcer/Documents/DiscordMemberNotifBot/data.json","r") as f:
            data = json.load(f)
        channels = data["users"][user_id]["message_count"]
        channel_data = {}
        for channel in channels.keys():
            count = channels[channel]["count"]
            if count != 0:
                channel_data[channels[channel]["name"]] = count

        fig1, ax1 = plt.subplots()
        ax1.pie(channel_data.values(),labels=channel_data.keys(),autopct=make_autopct(channel_data.values()),colors=['#7289DA','#2c2f33','#99aab5','#23272A'])
        ax1.axis('equal')
        plt.savefig('chart.png')
        await ctx.send(file=discord.File('chart.png'))
    elif target == "channel":
        with open("/Users/glebsvarcer/Documents/DiscordMemberNotifBot/data.json","r") as f:
            data = json.load(f)
        users = data["users"]
        
        user_data = {}

        for user in users.keys():
            channels = users[user]["message_count"]
            for channel in channels.keys():
                if channels[channel]["name"] == name:
                    count = channels[channel]["count"]
                    if count != 0:
                        user_data[users[user]["name"]] = count
                    break

        fig1, ax1 = plt.subplots()
        ax1.pie(user_data.values(),labels=user_data.keys(),autopct=make_autopct(user_data.values()),colors=['#7289DA','#2c2f33','#99aab5','#23272A'])
        ax1.axis('equal')
        plt.savefig('chart.png')
        await ctx.send(file=discord.File('chart.png'))
    elif target == "all":
        with open("/Users/glebsvarcer/Documents/DiscordMemberNotifBot/data.json","r") as f:
            data = json.load(f)
        
        if name == "users":

            channel_data = {}

            for user in users.keys():
                name = users

bot.run(TOKEN)