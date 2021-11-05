import discord, os, random, datetime, json
from discord.ext import commands, tasks
from discord.utils import get
from datetime import timezone, tzinfo, timedelta
from dotenv import load_dotenv
from os import system

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='//', activity=discord.Activity(name='//help', type=discord.ActivityType.listening), status=discord.Status.online)
bot.remove_command('help')

help_file = open('files/help.txt', 'r')
lines = help_file.readlines()

responses_file = open('files/responses.txt', 'r')
responses = responses_file.readlines()[:-1]

ranges = {None: [0,1,15],
         'test': [16,17,22],
         'fun': [23,24,38],
         'hm': [39,40,60],
         'note': [61,62,73],
         'audio': [74,75,98]}

json_file = 'files/servers.json'

def get_short_user(id):
    return str(id)[:-5]

def open_json(filename=json_file):
    with open(json_file, 'r+') as f:
        return json.load(f)

def write_json(data, filename=json_file):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_index_reversed(text, char):
    for i in range(len(text)-1,-1,-1):
        if text[i] == char:
            return i
    return None

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user} \nReady to run bot!')
    print('Current Servers')
    data = open_json()
    for i in bot.guilds:
        print(f'- "{i.name}" with {i.member_count} members')
        if i.name not in data:
            data[i.name] = {'members': i.member_count,
                            'ratings': {'good': 0, 'bad': 0},
                            'notes': [],
                            'hangman': {'active': False, 'pick': None, 'current': None, 'correct': [], 'incorrect': [], 'counter': 0},
                            'queue': []}
    write_json(data)

@bot.event
async def on_guild_join(self, guild):
    print(f'Joined: {guild.name}')
    data = open_json()
    if guild.name not in data:
        data[i.name] = {'members': i.member_count,
                        'ratings': {'good': 0, 'bad': 0},
                        'notes': [],
                        'hangman': {'active': False, 'pick': None, 'current': None, 'correct': [], 'incorrect': [], 'counter': 0},
                        'queue': []}
    write_json(data)

@bot.command()
async def help(ctx, section=None):
    final = ''
    bounds = [0,0,0] #title, upper, lower

    if section in ranges:
        bounds[0], bounds[1], bounds[2] = ranges[section][0], ranges[section][1], ranges[section][2]
        if section == None and isinstance(ctx.channel, discord.channel.DMChannel) == False:
            await ctx.send(f'A DM with the help sections has been sent, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'Help section not identified, {get_short_user(ctx.message.author)}')
        return

    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        await ctx.author.send(f'DM me help commands to avoid server spam, {get_short_user(ctx.message.author)}')

    for i in range(bounds[1], bounds[2]):
        final += lines[i]
    final = discord.Embed(title=lines[bounds[0]], description=final, color=discord.Color.from_rgb(200,0,0))
    await ctx.author.send(embed=final)

### Test ###
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms', )

@bot.command(aliases=['dt'])
async def date_time(ctx):
    currentDate = datetime.datetime.now()
    date = currentDate.strftime("%A, %d of %B of %Y")
    time = currentDate.strftime("%I:%M:%S %p")

    await ctx.send(f'Current date is: {date}')
    await ctx.send(f'Current time is: {time}')


### Fun ###
@bot.command()
async def echo(ctx, *, message=None):
    if message == None:
        await ctx.send(f'No text provided, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'{get_short_user(ctx.message.author)} said: {message}')

@bot.command(aliases=['rng'])
async def random_number_generator(ctx, num:int=None):
    if num == None:
        await ctx.send(f'No number selected, {get_short_user(ctx.message.author)}')
    elif num < 1:
        await ctx.send(f'Invalid number selected, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'Number randomly generated between 1 and {num}: {random.randint(1,num)}')

@bot.command(aliases=['8ball'])
async def _8Ball(ctx, *, question=None):
    if question == None:
        await ctx.send(f'No question asked, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'||{random.choice(responses)[:-1]}, {get_short_user(ctx.message.author)}||')

@bot.command()
async def dice(ctx):
    dices = ["⚀","⚁","⚂","⚃","⚄","⚅"]
    values = [random.choice(dices), random.choice(dices)]

    await ctx.send(f'{values[0]} {values[1]}')
    
    await ctx.send(f'{get_short_user(ctx.message.author)}\'s total value of dices: {(dices.index(values[0])+1) + (dices.index(values[1])+1)}')

    if values[0] == values[1]:
        await ctx.send('You got pairs!')

@bot.command(aliases=['rps'])
async def rock_paper_scissors(ctx, user_decision=None):
    if user_decision == None:
        await ctx.send(f'No decision made, {get_short_user(ctx.message.author)}')
        return
    elif len(user_decision) > 1:
        await ctx.send(f'Invalid decision, {get_short_user(ctx.message.author)}')
        return

    choices = 'rps'

    if user_decision not in choices:
        await ctx.send(f'Invalid decision, {get_short_user(ctx.message.author)}')
        return

    bot_decision = choices[random.randint(0,2)]

    names = {'r': 'rock', 'p': 'paper', 's': 'scissors'}

    await ctx.send(f'You chose {names[user_decision]} and I chose {names[bot_decision]}')

    user_index = choices.index(user_decision)
    bot_index = choices.index(bot_decision)

    if user_index == 0 and bot_index == 2:
        await ctx.send('You win!')
    elif (bot_index == 0 and user_index == 2) or bot_index > user_index:
        await ctx.send('You lose!')
    elif user_index > bot_index:
        await ctx.send('You win!')
    elif user_index == bot_index:
        await ctx.send('It\'s a tie!')


### Hangman ###
@bot.command(aliases=['hmcreate'])
async def hangman_create(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        if data[ctx.message.guild.name]['hangman']['active'] == False:
            data[ctx.message.guild.name]['hangman']['active'] = True
            write_json(data)
            await ctx.send(f'A DM with the instructions has been sent, {get_short_user(ctx.message.author)}')
            await ctx.author.send('Use the following command to select the word or words to play with (copy until server name and encase your word/s in parenthesis):')
            await ctx.author.send(f'`//hmpick {ctx.message.guild.name} ("word or words")`')
        else:
            await ctx.send(f'Hangman game already active, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['hmpick'])
async def hangman_pick(ctx, *, message=None):
    if message == None:
        await ctx.author.send('Use the following command to select the word or words to play with (copy until server name and encase your word/s in parenthesis):')
        await ctx.author.send(f'`//hmpick {ctx.message.guild.name} ("word or words")`')
    elif message[-1] != ')':
        await ctx.send(f'Invalid format used, {get_short_user(ctx.message.author)}')
        await ctx.author.send('Use the following command to select the word or words to play with (copy until server name and encase your word/s in parenthesis):')
        await ctx.author.send(f'`//hmpick {ctx.message.guild.name} ("word or words")`')
    else:
        left_par_idx = get_index_reversed(message, '(')
        if left_par_idx == None:
            await ctx.send(f'Invalid format used, {get_short_user(ctx.message.author)}')
            await ctx.author.send('Use the following command to select the word or words to play with (copy until server name and encase your word/s in parenthesis):')
            await ctx.author.send(f'`//hmpick {ctx.message.guild.name} ("word or words")`')
        else:
            server = message[:left_par_idx-1]
            data = open_json()
            if server not in data:
                await ctx.send(f'No server with such name found, {get_short_user(ctx.message.author)}')
            elif data[server]['hangman']['active'] == False:
                await ctx.send(f'No active hangman game, {get_short_user(ctx.message.author)}')
            elif data[server]['hangman']['pick'] != None:
                await ctx.send(f'Pick already chosen, {get_short_user(ctx.message.author)}')
            else:
                data[server]['hangman']['pick'] = message[left_par_idx+1:-1]
                tmp = ''
                for i in data[server]['hangman']['pick']:
                    if i.isalpha() == True:
                        tmp += '_ '
                    else:
                        tmp += f'{i} '
                tmp = tmp[:-1]
                data[server]['hangman']['current'] = tmp
                write_json(data)
                await ctx.send(f'Current hangman pick is: *{data[server]["hangman"]["pick"]}*')
                await ctx.send('Use the following command to show the game in the server:')
                await ctx.send('`//hmshow`')

@bot.command(aliases=['hmshow'])
async def hangman_show(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        server = ctx.author.guild.name
        if data[server]['hangman']['active'] == False:
            await ctx.send(f'No active hangman game, {get_short_user(ctx.message.author)}')
        elif data[server]['hangman']['pick'] == None:
            await ctx.send(f'Word hasn\'t been picked yet, {get_short_user(ctx.message.author)}')
        else:
            check = len(data[server]["hangman"]["incorrect"]) + data[server]["hangman"]["counter"]
            await ctx.send(file=discord.File(f'images/hangman_{check}.png'))
            await ctx.send(f'`{data[server]["hangman"]["current"]}`')
            if check == 6:
                await ctx.send('Game over, you lost...')
                data[server]['hangman'] = {'active': False, 'pick': None, 'current': None, 'correct': [], 'incorrect': [], 'counter': 0}
                write_json(data)
            elif '_' not in data[server]['hangman']['current']:
                await ctx.send('Game over, you won!')
                data[server]['hangman'] = {'active': False, 'pick': None, 'current': None, 'correct': [], 'incorrect': [], 'counter': 0}
                write_json(data)
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['hml'])
async def hangman_letter(ctx, *, letter=None):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        server = ctx.author.guild.name
        if data[server]['hangman']['active'] == False:
            await ctx.send(f'No active hangman game, {get_short_user(ctx.message.author)}')
        elif letter == None:
            await ctx.send(f'You\'re missing a letter, {get_short_user(ctx.message.author)}')
        elif len(letter) > 1:
            await ctx.send(f'You can only choose one letter at a time, {get_short_user(ctx.message.author)}')
        elif letter.isalpha() == False:
            await ctx.send(f'Invalid letter chosen, {get_short_user(ctx.message.author)}')
        else:
            correct = data[server]['hangman']['correct']
            incorrect = data[server]['hangman']['incorrect']
            if letter in correct or letter in incorrect:
                await ctx.send(f'Letter already chosen, {get_short_user(ctx.message.author)}')
            else:
                positions = [i[0]*2 for i in enumerate(data[server]['hangman']['pick']) if i[1] == letter]
                if len(positions) == 0:
                    await ctx.send(f'"{letter}" is not in the word, {get_short_user(ctx.message.author)}')
                    data[server]['hangman']['incorrect'].append(letter)
                    write_json(data)
                    await ctx.invoke(bot.get_command('hmshow'))
                else:
                    current = list(data[server]['hangman']['current'])
                    for i in positions:
                        current[i] = letter
                    current = ''.join(current)
                    await ctx.send(f'"{letter}" is in the word, {get_short_user(ctx.message.author)}')
                    data[server]['hangman']['correct'].append(letter)
                    data[server]['hangman']['current'] = current
                    write_json(data)
                    await ctx.invoke(bot.get_command('hmshow'))
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['hmguess'])
async def hangman_guess(ctx, *, message=None):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        server = ctx.author.guild.name
        if data[server]['hangman']['active'] == False:
            await ctx.send(f'No active hangman game, {get_short_user(ctx.message.author)}')
        elif message == None:
            await ctx.send(f'No text was given, {ctx.message.author}')
        else:
            if data[server]['hangman']['pick'] == message:
                await ctx.send(f'Correct guess, {get_short_user(ctx.message.author)}')
                tmp = ''
                for i in message:
                    tmp += f'{i} '
                data[server]['hangman']['current'] = tmp
                write_json(data)
                await ctx.invoke(bot.get_command('hmshow'))
            else:
                await ctx.send(f'Incorrect guess, {get_short_user(ctx.message.author)}')
                data[server]['hangman']['counter'] += 1
                write_json(data)
                await ctx.invoke(bot.get_command('hmshow'))
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['hmgm'])
async def hangman_guesses_misses(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        server = ctx.author.guild.name
        if data[server]['hangman']['active'] == False:
            await ctx.send(f'No active hangman game, {get_short_user(ctx.message.author)}')
        else:
            await ctx.send('Current guesses:')
            await ctx.send(data[server]['hangman']['correct'])
            await ctx.send('Current misses:')
            await ctx.send(data[server]['hangman']['incorrect'])
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['hmdelete'])
async def hangman_delete(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        server = ctx.author.guild.name
        if data[server]['hangman']['active'] == False:
            await ctx.send(f'No active hangman game, {get_short_user(ctx.message.author)}')
        else:
            data[server]['hangman'] = {'active': False, 'pick': None, 'current': None, 'correct': [], 'incorrect': [], 'counter': 0}
            write_json(data)
            await ctx.send(f'Current game deleted, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')


### Notes ###
@bot.command()
async def notes(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        tmp = data[ctx.message.guild.name]['notes']
        if len(tmp) == 0:
            await ctx.send(f'No server notes to display, {get_short_user(ctx.message.author)}')
        else:
            await ctx.send(f'**{ctx.message.guild.name} notes**')
            for i, note in enumerate(tmp):
                await ctx.send(f'**{i+1}.** {note["author"]} on {note["date"]}:\n-  {note["message"]}')
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['cnote'])
async def create_note(ctx, *, message=None):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        if message == None:
            await ctx.send(f'No text provided, {get_short_user(ctx.message.author)}')
        else:
            data = open_json()
            currentDate = datetime.datetime.now()
            date = currentDate.strftime("%A, %d of %B of %Y")
            time = currentDate.strftime("%I:%M:%S %p")
            data[ctx.message.guild.name]['notes'].append({'author': get_short_user(ctx.message.author), 
                                                          'date': f'{date} at {time}',
                                                          'message': message})
            write_json(data)
            await ctx.send(f'Note added, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['dnote'])
async def delete_note(ctx, position:int=None):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        if position == None:
            await ctx.send(f'No position provided, {get_short_user(ctx.message.author)}')
        data = open_json()
        tmp = data[ctx.message.guild.name]['notes']
        if len(tmp) == 0 or position > len(tmp) or position <= 0:
            await ctx.send(f'Note index out of range, {get_short_user(ctx.message.author)}')
        else:
            data[ctx.message.guild.name]['notes'].pop(position-1)
            write_json(data)
            await ctx.send(f'Note deleted, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')

@bot.command(aliases=['rnotes'])
async def remove_notes(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) == False:
        data = open_json()
        tmp = data[ctx.message.guild.name]['notes']
        if len(data[ctx.message.guild.name]['notes']) == 0:
            await ctx.send(f'No notes to remove, {get_short_user(ctx.message.author)}')
        else:
            data[ctx.message.guild.name]['notes'] = []
            write_json(data)
            await ctx.send(f'All notes removed, {get_short_user(ctx.message.author)}')
    else:
        await ctx.send(f'You\'re not currently in a server, {get_short_user(ctx.message.author)}')


### Audio ###
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *, message=None):
    pass

@bot.command()
async def resume(ctx):
    pass

@bot.command()
async def pause(ctx):
    pass

@bot.command()
async def stop(ctx):
    pass

@bot.command()
async def next(ctx):
    pass

@bot.command()
async def volume(ctx, *, message:int=None):
    pass

# @bot.event
# async def on_guild_join(guild):

@bot.event
async def on_message(message):
    # if isinstance(message.channel, discord.channel.DMChannel) == False:
    # if message.guild != None:
    #     print(f'{message.author} from "{message.guild.name}": {message.content}')
    # else:
    #     print(f'{message.author} from "Direct Message Channel": {message.content}')

    # if message.content.startswith(f'<@!{bot.user.id}>'):
    #     await message.channel.send(f'You called, {get_short_user(message.author)}?')

    if message.guild != None:
        if message.content.startswith('good bot'):
            data = open_json()
            data[message.guild.name]['ratings']['good'] += 1
            write_json(data)
            await message.channel.send('Glad to hear that :smile:')
            await message.channel.send(f'Current positive ratings: {data[message.guild.name]["ratings"]["good"]}')
            await message.channel.send(f'Current negative ratings: {data[message.guild.name]["ratings"]["bad"]}')
        elif message.content.startswith('bad bot'):
            data = open_json()
            data[message.guild.name]['ratings']['bad'] += 1
            write_json(data)
            await message.channel.send('Sorry to hear that :confused:')
            await message.channel.send(f'Current positive ratings: {data[message.guild.name]["ratings"]["good"]}')
            await message.channel.send(f'Current negative ratings: {data[message.guild.name]["ratings"]["bad"]}')

    # if message.author != bot.user:
    #     await message.channel.send(f'User test: {short_user(message.author)}')

    await bot.process_commands(message)

bot.run(TOKEN)