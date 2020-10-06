import discord
import random
import youtube_dl
import os
import shutil
import datetime
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from datetime import timezone,tzinfo,timedelta
from os import system

TOKEN = ""

bot = commands.Bot(command_prefix="//")
bot.remove_command("help")
bot.remove_command("next")

#status = cycle(["your commands","//help"])

listNotes = []

queues = {}

hangmanWord = []
displayGuess = ["`"]
guessPositions = []
playerGuesses = []
playerMisses = []
onlineHangman = False
triesInt = 0

listUsers = []

good = 0
bad = 0

hangmanTries = ["hangman_0.png","hangman_1.png","hangman_2.png","hangman_3.png","hangman_4.png","hangman_5.png","hangman_6.png"]

helpPage = """**Test Commands:**\n
> `//ping`
> Returns pong and bot's latency\n
> `//dt`
> Displays the current date and time\n
\n**Fun Commands:**\n
> `//echo (text)`
> Returns what was said in the text\n
> `//rng (number)`
> Generates a random number between 1 and the selected number\n
> `//8ball (question)`
> Returns an 8ball answer to a question\n
> `//dice`
> Roll a pair of dices\n
> `//rps (text)`
> Play rock, paper scissors against the bot (text has to be either 'r', 'p' or 's')\n
\n**Hangman Commands:**\n
> `//hmcreate`
> Creates a hangman game\n
> `//hmpick`
> Picks the word for the game (it's recommended to send a DM to the bot with this command)\n
> `//hmshow`
> Displays current game\n
> `//hml (letter)`
> Shows whether the letter is in the word or not\n
> `//hmguess (word or words)`
> Shows whether the guessed words is correct or not\n
> `//hmgm`
> Displays all guesses and misses\n
> `//hmdelete`
> Deletes current game\n
\n**Note Commands:**\n
> `//notes`
> Displays list of notes\n
> `//cnote`
> Create a note with the text given\n
> `//dnote`
> Deletes a note in the position of the number selected (it's recommended to view all notes before using this command)\n
> `//rnotes`
> Deletes all notes from the list\n
\n**Audio Commands:**\n
> `//join`
> Makes bot join current channel\n
> `//leave`
> Makes bot leave current channel\n
> `//play (youtube song or audio name)`
> Plays audio from message in command\n
> `//queue (youtube song or audio name)`
> Queues audio from message in command\n
> `//resume`
> Resumes current audio\n
> `//pause`
> Pauses current audio\n
> `//stop`
> Fully stops current audio and queue from playing\n
> `//next`
> Plays next audio in queue\n
> `//volume (number)`
> Switches audio to stated number percentage\n
\n**Ratings:**\n
> `'good bot'`
> Rate my performance by typing 'good bot' in chat\n
> `'bad bot'`
> Rate my performance by typing 'bad bot' in chat\n"""

def short_user(id):

    listUsername = list(str(id))
    for _ in range(5):
        listUsername.remove(listUsername[-1])
    username = "".join(listUsername)
    return(username)

@bot.event
async def on_ready():

    print(f"Logged in as: {bot.user} \nReady to run bot!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" //help"))
    #change_status.start()

#@tasks.loop(seconds=4)
#async def change_status():
#
#    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(status)))

@bot.command()
async def help(ctx):

    await ctx.send(f"A DM with all the commands has been sent, {short_user(ctx.message.author)}")
    await ctx.author.send(helpPage)

@bot.command()
async def ping(ctx):

    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(aliases=["dt"])
async def date_time(ctx):
    currentDate = datetime.datetime.now()
    date = currentDate.strftime("%A, %d of %B of %Y")
    time = currentDate.strftime("%I:%M:%S %p")
    checkSpecial = currentDate.strftime("%d of %B")

    await ctx.send(f"**Current date:** {date}\n**Current time:** {time}")
    if checkSpecial == "01 of January":
        await ctx.send(":fireworks: Happy New Year! :fireworks:")
    elif checkSpecial == "14 of February":
        await ctx.send(":sparkling_heart: Happy Valentine's Day! :sparkling_heart:")
    elif checkSpecial == "01 of April":
        await ctx.send(":clown: !sloof lirpA :clown:")
    elif checkSpecial == "12 of September":
        await ctx.send(":video_game: Happy Video Games Day! :video_game:")
    elif checkSpecial == "31 of October":
        await ctx.send(":ghost: Happy Halloween! :ghost:")
    elif checkSpecial == "25 of December":
        await ctx.send(":christmas_tree: Merry Christmas! :christmas_tree:")
    elif checkSpecial == "31 of December":
        await ctx.send(":calendar_spiral: See you next year! :calendar_spiral:")


@bot.command()
async def echo(ctx,*,message:str):

    await ctx.send(message)

@bot.command(aliases=["rng"])
async def random_number_generator(ctx,number:int):

    result = random.randint(1,number)

    await ctx.send(f"**Number randomly generated bewteen 1 and {number}:** {result}")

@bot.command(aliases=["8ball"])
async def _8Ball(ctx,*, question:str):

    responses = ["As I see it, yes",
                 "Ask again later",
                 "Better not tell you now",
                 "Cannot predict now",
                 "Concentrate and ask again",
                 "Don’t count on it",
                 "It is certain",
                 "It is decidedly so",
                 "Most likely",
                 "My reply is no",
                 "My sources say no",
                 "Outlook not so good",
                 "Outlook good",
                 "Reply hazy, try again",
                 "Signs point to yes",
                 "Very doubtful",
                 "Without a doubt",
                 "Yes",
                 "Yes, definitely",
                 "You may rely on it"]
    
    await ctx.send(f"**Question:** {question}\n**Answer:** || {random.choice(responses)}, {short_user(ctx.message.author)} ||")

@bot.command()
async def dice(ctx):

    dices = ["⚀","⚁","⚂","⚃","⚄","⚅"]

    diceOne = random.choice(dices)
    diceTwo = random.choice(dices)

    await ctx.send(f"{diceOne}\n{diceTwo}")

    valueOne = dices.index(diceOne) + 1
    valueTwo = dices.index(diceTwo) + 1

    total = valueOne + valueTwo
    await ctx.send(f"**{short_user(ctx.message.author)}'s total value of dices:** {total}")
    if valueOne == valueTwo:
        await ctx.send("You got pairs!")

@bot.command(aliases=["rps"])
async def rock_paper_scissors(ctx,decision:str):

    rpsBot = ["r","p","s"]
    decisionBot = random.choice(rpsBot)

    bothChoices = f"You chose {decision} and I chose {decisionBot}"
    winBot = "I won!"
    winHuman = "You won!"

    if decision == decisionBot:
        await ctx.send(bothChoices)
        await ctx.send("It's a tie!")
    elif decision == "r" and decisionBot == "p":
        await ctx.send(bothChoices)
        await ctx.send(winBot)
    elif decision == "r" and decisionBot == "s":
        await ctx.send(bothChoices)
        await ctx.send(winHuman)
    elif decision == "p" and decisionBot == "r":
        await ctx.send(bothChoices)
        await ctx.send(winHuman)
    elif decision == "p" and decisionBot == "s":
        await ctx.send(bothChoices)
        await ctx.send(winBot)
    elif decision == "s" and decisionBot == "r":
        await ctx.send(bothChoices)
        await ctx.send(winBot)
    elif decision == "s" and decisionBot == "p":
        await ctx.send(bothChoices)
        await ctx.send(winHuman)


@bot.command(aliases=["hmcreate"])
async def hangman_create(ctx):

    global onlineHangman

    if onlineHangman == True:
        await ctx.send(f"A game is already in progress, {short_user(ctx.message.author)}\nTo create a new game, delete the current one")
    else:
        await ctx.send(f"{short_user(ctx.message.author)}, a DM with the instructions to start the hangman game has been sent to you")
        await ctx.author.send(f"Hello {short_user(ctx.message.author)}, to pick a word, type in this chat:\n`//hmpick (word or words)`")
        onlineHangman = True

@bot.command(aliases=["hmpick"])
async def hangman_pick(ctx,*,pick:str):

    global onlineHangman
    global hangmanWord
    global displayGuess
    global guessPositions
    global triesInt
    positionsDiscord = 1
    specialCharacters = [" ","-","&","%","$","!","¡","?","¿","'","´"]

    if onlineHangman == True and len(hangmanWord) == 0:
        for i in range(len(pick)):
            hangmanWord.append(pick.lower()[i])
            displayGuess.append("_")
            if i != len(pick)-1:
                displayGuess.append(" ")
            guessPositions.append(positionsDiscord)
            positionsDiscord += 2
        displayGuess.append("`")
        await ctx.author.send("**You chose the word/s:**")
        await ctx.author.send("".join(hangmanWord))
        for y in range(len(specialCharacters)):
            if specialCharacters[y] in hangmanWord:
                positions = [i for i, x in enumerate(hangmanWord) if x == specialCharacters[y]]
                for i in range(len(positions)):
                    displayGuess[guessPositions[positions[i]]] = specialCharacters[y]

        await ctx.send(" ⠀ \nUse the following command in the server to show the game:\n`//hmshow`")
    elif len(hangmanWord) > 0:
        await ctx.send(f"Sorry {short_user(ctx.message.author)}, a word has already been chosen")
    else:
        await ctx.author.send(f"Sorry {short_user(ctx.message.author)}, a game has not been created yet")

@bot.command(aliases=["hmdelete"])
async def hangman_delete(ctx):
     
    global onlineHangman
    global hangmanWord
    global displayGuess
    global guessPositions
    global triesInt

    if onlineHangman == True:
        onlineHangman = False
        hangmanWord.clear()
        displayGuess.clear()
        guessPositions.clear()
        triesInt = 0
        playerGuesses.clear()
        playerMisses.clear()
        displayGuess.append("`")
        await ctx.send(f"Current game was deleted by {short_user(ctx.message.author)}")
    else:
        await ctx.send(f"No game to delete, {short_user(ctx.message.author)}")

@bot.command(aliases=["hmshow"])
async def hangman_show(ctx):

    global onlineHangman
    global hangmanWord
    global displayGuess
    global guessPositions
    global triesInt

    if onlineHangman == True:
        await ctx.send(file=discord.File(hangmanTries[triesInt]))
        await ctx.send("".join(displayGuess))
    else:
        await ctx.send(f"No game to show, {short_user(ctx.message.author)}")

@bot.command(aliases=["hml"])
async def hangman_guess_letter(ctx,letter:str):
    
    global onlineHangman
    global hangmanWord
    global displayGuess
    global guessPositions
    global triesInt
    global playerGuesses
    global playerMisses


    if onlineHangman == True:
        if len(letter) > 1:
            await ctx.send(f"Only one letter, {short_user(ctx.message.author)}")
        else:
            if (letter in playerGuesses) or (letter in playerMisses):
                await ctx.send("already used that letter")
            else:
                await ctx.send(f"{short_user(ctx.message.author)} guessed the letter {letter} ...")
                if letter in hangmanWord:
                    await ctx.send("which is in the word")
                    positions = [i for i, x in enumerate(hangmanWord) if x == letter]
                    for i in range(len(positions)):
                        displayGuess[guessPositions[positions[i]]] = letter
                    playerGuesses.append(letter)
                    
                    await ctx.send(file=discord.File(hangmanTries[triesInt]))
                    await ctx.send("".join(displayGuess))
                    if "_" not in displayGuess:
                        await ctx.send("You won!")
                        onlineHangman = False
                        hangmanWord.clear()
                        displayGuess.clear()
                        guessPositions.clear()
                        triesInt = 0
                        playerGuesses.clear()
                        playerMisses.clear()
                        displayGuess.append("`")
                else:
                    await ctx.send("which is not in the word")
                    triesInt += 1
                    playerMisses.append(letter)
                    await ctx.send(file=discord.File(hangmanTries[triesInt]))
                    await ctx.send("".join(displayGuess))
                    if triesInt == 6:
                        await ctx.send("You lost!")
                        await ctx.send("The word was:")
                        await ctx.send("".join(hangmanWord))
                        onlineHangman = False
                        hangmanWord.clear()
                        displayGuess.clear()
                        guessPositions.clear()
                        triesInt = 0
                        playerGuesses.clear()
                        playerMisses.clear()
                        displayGuess.append("`")
    else:
        await ctx.send(f"Can't guess a letter without a game, {short_user(ctx.message.author)}")

@bot.command(aliases=["hmgm"])
async def hangman_guesses_misses(ctx):

    global onlineHangman
    global playerGuesses
    global playerMisses

    if onlineHangman == True:
        await ctx.send("**Guesses:**")
        if len(playerGuesses) != 0:
            await ctx.send(", ".join(playerGuesses))
        else:
            await ctx.send("no guesses yet")

        await ctx.send("**Misses:**")
        if len(playerMisses) != 0:
            await ctx.send(", ".join(playerMisses))
        else:
            await ctx.send("no misses yet")
    else:
        await ctx.send(f"No guesses or misses to show, {short_user(ctx.message.author)}")

@bot.command(aliases=["hmguess"])
async def hangman_guess_word(ctx,*,word):

    global onlineHangman
    global hangmanWord
    global displayGuess
    global guessPositions
    global triesInt
    finalWord = "".join(word)
    finalHangman = "".join(hangmanWord)

    if onlineHangman == True:
        await ctx.send(f"{short_user(ctx.message.author)} guessed the word {word} ...")
        if finalWord == finalHangman:
            await ctx.send("which is correct")
            await ctx.send(file=discord.File(hangmanTries[triesInt]))
            finalDisplay = ["`"]
            for i in range(len(word)):
                finalDisplay.append(word[i])
                if i != len(word)-1:
                    finalDisplay.append(" ")
            finalDisplay.append("`")
            await ctx.send("".join(finalDisplay))
            await ctx.send("You guessed it!")
            onlineHangman = False
            hangmanWord.clear()
            displayGuess.clear()
            guessPositions.clear()
            triesInt = 0
            playerGuesses.clear()
            playerMisses.clear()
            displayGuess.append("`")
        else:
            await ctx.send("which is incorrect")
            triesInt += 1
            await ctx.send(file=discord.File(hangmanTries[triesInt]))
            await ctx.send("".join(displayGuess))
            if triesInt == 6:
                await ctx.send("You lost!")
                await ctx.send("The word was:")
                await ctx.send("".join(hangmanWord))
                onlineHangman = False
                hangmanWord.clear()
                displayGuess.clear()
                guessPositions.clear()
                triesInt = 0
                playerGuesses.clear()
                playerMisses.clear()
                displayGuess.append("`")
    else:
        await ctx.send(f"Can't guess a word without a game, {short_user(ctx.message.author)}")


@bot.command()
async def notes(ctx):

    global listNotes

    if not listNotes:
        await ctx.send(f"No notes available to display, {short_user(ctx.message.author)}")
    else:
        for i in range(len(listNotes)):
            if i == 0:
                await ctx.send(listNotes[i])
            else:
                await ctx.send(f" ⠀ \n{listNotes[i]}")

@bot.command(aliases=["cnote"])
async def create_note(ctx,*,message:str):

    global listNotes
    currentDate = datetime.datetime.now()
    date = currentDate.strftime("%A, %d of %B of %Y")
    time = currentDate.strftime("%I:%M:%S %p")

    listNotes.append(f"**Note by {short_user(ctx.message.author)} on {date} at {time}:**\n{message}")
    await ctx.send(f"Note added , {short_user(ctx.message.author)}!")

@bot.command(aliases=["dnote"])
async def delete_note(ctx,position:int):

    global listNotes

    if not listNotes:
        await ctx.send(f"No note left to delete ,{short_user(ctx.message.author)}")
    else:
        if len(listNotes) >= position:
            listNotes.remove(listNotes[position-1])
            await ctx.send(f"Note on position #{position} removed ,{short_user(ctx.message.author)}!")
        else:
            await ctx.send(f"Note on position #{position} does not exist ,{short_user(ctx.message.author)}")

@bot.command(aliases=["rnotes"])
async def reset_notes(ctx):

    global listNotes

    if not listNotes:
        await ctx.send(f"Note list is currently empty ,{short_user(ctx.message.author)}")
    else:
        for _ in range(len(listNotes)):
            listNotes.remove(listNotes[-1])
        await ctx.send(f"Note list has been emptied out, {short_user(ctx.message.author)}")


@bot.command()
async def join(ctx):

    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send(f"{short_user(ctx.message.author)}, you are currently not connected to a voice channel")
    global vc
    try:
        vc=await channel.connect()
        await ctx.send(f"**Joined voice channel:** {channel}")
    except:
        TimeoutError 

@bot.command()
async def leave(ctx):

    channel = ctx.author.voice.channel
    try:
        if vc.is_connected():
            await vc.disconnect()
            await ctx.send(f"**Left voice channel:** {channel}")
    except:
        TimeoutError
        pass

@bot.command()
async def play(ctx,*,url: str):

    await ctx.send(f"Downloading audio now, {short_user(ctx.message.author)}\nPlease do not use any other commands in the meantime")

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'outtmpl': "./song.mp3",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_search = " ".join(url)
    errorExit = 0

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([f"ytsearch1:{song_search}"])
    except:
        errorExit += 1

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    if errorExit == 1:
        await ctx.send(f"Sorry {short_user(ctx.message.author)}, I can't find anything with that name")
    else:
        await ctx.send(f":loud_sound: Playing audio now :loud_sound:")

@bot.command()
async def playurl(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

@bot.command()
async def queue(ctx,*,url: str):

    await ctx.send(f"Downloading audio now, {short_user(ctx.message.author)}\nPlease do not use any other commands in the meantime")

    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_search = " ".join(url)
    errorExit = 0

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([f"ytsearch1:{song_search}"])
    except:
        errorExit += 1

    if errorExit == 1:
        await ctx.send(f"Sorry {short_user(ctx.message.author)}, I can't find anything with that name")
    else:
        await ctx.send(f":hourglass: Adding song to the queue, {short_user(ctx.message.author)} :hourglass:")

@bot.command()
async def queueurl(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Adding song " + str(q_num) + " to the queue")

@bot.command()
async def pause(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        await ctx.send(f":play_pause: Audio paused by {short_user(ctx.message.author)} :play_pause:")
    else:
        await ctx.send(f"Audio's currently not playing {short_user(ctx.message.author)}")

@bot.command()
async def resume(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        await ctx.send(f":play_pause: Audio resumed by {short_user(ctx.message.author)} :play_pause:")
    else:
        await ctx.send(f"Audio's currently not paused {short_user(ctx.message.author)}")

@bot.command()
async def stop(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if (voice and voice.is_paused()) or (voice and voice.is_playing()):
        voice.stop()
        await ctx.send(f":mute: Audio stopped by {short_user(ctx.message.author)} :mute:")
    else:
        await ctx.send(f"No audio to stop ,{short_user(ctx.message.author)}")

@bot.command()
async def next(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    if (voice and voice.is_paused()) or (voice and voice.is_playing()):
        voice.stop()
        await ctx.send(f":track_next: Playing next song :track_next:")
    else:
        await ctx.send(f"No audio can be played next, {short_user(ctx.message.author)}")

@bot.command()
async def volume(ctx,volume:int):
    if ctx.voice_client is None:
        return await ctx.send(f"{short_user(ctx.message.author)}, you are currently not connected to a voice channel")
    
    ctx.voice_client.source.volume = volume/100
    await ctx.send(f":sound: {short_user(ctx.message.author)} changed audios volume to {volume}% :sound:")


@bot.event
async def on_message(message):

    print(f"{message.author}: {message.content}\n")

    #Ratings
    global good
    global bad
    if message.content.startswith("good bot"):
        good += 1
        await message.channel.send(f"I'm glad to hear that, {short_user(message.author)} :heart:\nI'll keep it up!\n**Current bot ratings:**")
        await message.channel.send(f" ⠀ \n:slight_smile:  {good}\n\n:slight_frown:  {bad}")
    elif message.content.startswith("bad bot"):
        bad += 1
        await message.channel.send(f"I'm sorry to hear that, {short_user(message.author)} :broken_heart:\nI'll try better next time...\n**Current bot ratings:**")
        await message.channel.send(f" ⠀ \n:slight_smile:  {good}\n\n:slight_frown:  {bad}")
    
    #Messages to chat with bot
    if message.content.startswith(f"<@!{bot.user.id}>"):
        await message.channel.send(f"You called, {short_user(message.author)}?")

    await bot.process_commands(message)


bot.run(TOKEN)