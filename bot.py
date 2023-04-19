import discord
import time
from lyricsgenius import Genius

# Sets the genius api key
with open("geniusapi.txt", "r") as apitxt:
    api = apitxt.read()
    genius = Genius(api, timeout=60)


# Makes a function for getting the current unix timestamp
def unix_timestamp():
    timestamp = int(time.time())
    return timestamp


# Sets the intens the bot wants to use
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Starts the bot client witht he intents we set
bot = discord.Bot(intents=intents)
# Variable for enabling/disabling logging
logging = True


# Logs that the bot is online when it's ready
@bot.event
async def on_ready():
    print(f"The script is running on bot {bot.user}")


# Checks for messages
@bot.event
async def on_message(message):
    # Sets a channel for logs
    log_channel = await bot.fetch_channel(997839935518281729)

    # Checks if the message authot is NOT the bot and the logging is True
    if message.author.bot != True and logging:
        # Retrieves the timestamp from the functioned defined earlier
        timestamp = unix_timestamp()

        # Code for making an embed
        async def embed():
            # Sets the embed title and description, also the color
            embed = discord.Embed(
                title=f"Message log from user {message.author}:",
                description=f"**Message content:**\n \
                {message.content} \n \
                **On:** \n \
                <t:{timestamp}:F>",
                color=discord.Color.blue(),
            )
            # Sends the embed
            await log_channel.send(embed=embed)

        await embed()


@bot.event
async def on_message_delete(message):
    log_channel = await bot.fetch_channel(997839935518281729)

    if message.author.bot != True and logging:
        timestamp = unix_timestamp()

        async def embed():
            embed = discord.Embed(
                title=f"Message deleted from user <@{message.author}>:",
                description=f"**Message content:**\n \
                {message.content} \n \
                **On:** \n \
                <t:{timestamp}:F>",
                color=discord.Color.red(),
            )
            await log_channel.send(embed=embed)

        await embed()


@bot.command(description="Just a command for Stefan keeping the active dev badge")
async def ooga(ctx):
    await ctx.respond("You used the ooga command!")


# * Discord bot command for enabling/disabling the logging feature
@bot.command(
    description="Disables or Enables the logging feature until the bot restarts"
)
async def log(ctx):
    # Retrieves the user who executed the command
    user = ctx.author
    # Sets the role we need the user to have to execute the command
    role = discord.utils.get(ctx.guild.roles, name="Cool People")
    # ! Do not remove this if statement, if removed, the bot will allow anyone to enable/disable logging
    # Checks if the role we set is in the rolelist of the user who executed the command, if the user is not authorised, give a proper error message
    if role in user.roles:
        # Checks if logging is true, then set it to false, if false, then set it to true, with a message to respond to the user
        global logging
        if logging:
            logging = False
            await ctx.respond("You disabled logging")
        else:
            logging = True
            await ctx.respond("You enabled logging")
    else:
        await ctx.respond("You do not have the permissions to execute this command!")


# * Discord bot command for searching lyrics
@bot.command(description="Searches for lyrics!")
async def lyrics(ctx, *, song):
    await ctx.respond(f"Searching lyrics for song: {song}")
    # Tries searching for the lyrics
    try:
        lyrics = genius.search_song(song).lyrics
    # If an except is thrown notify the user
    except TypeError:
        await ctx.channel.send("No lyrics found.")
        return

    # Chops the lyrics in chunks of maxmimum 2000 characters
    lyrics_chunks = [lyrics[i : i + 2000] for i in range(0, len(lyrics), 2000)]

    # Makes and sends the embed
    for i, chunk in enumerate(lyrics_chunks):
        embed = discord.Embed(
            title=f"Lyrics for {song}",
            description=chunk,
            color=discord.Color.green(),
        )
        if i == 0:
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed)


# ! Do not remove this line as it runs the bot
with open("token.txt", "r") as tokentxt:
    token = tokentxt.read()
    bot.run(token)
