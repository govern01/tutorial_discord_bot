from datetime import datetime
from configparser import ConfigParser
from discord.ext import commands
import logger_factory

# Tool to read ini files easier
cfg = ConfigParser()
cfg.read("bot.ini")
bot_cfg = cfg['BOT']

# Creates a bot object to pass commands, checks, cogs and anything else into
bot = commands.Bot(command_prefix=bot_cfg['command_prefix'])

# The chat_logger object
chat_logger = None


@bot.event
async def on_ready():
    """Event fires when bot is connected to discord and ready to take commands

    Here is where you should handle init/pre-init things, like generating chat loggers or random seeds(idk up to you
    what you put in here). If you also want to rewrite the generated help command you would drop it here.
    In this tutorial we are going to use this to handle chat logging.
    """
    global chat_logger
    chat_logger = logger_factory.generate_logger()
    cur = datetime.now()
    print(f"[{cur.strftime('%H:%M:%S')}] Bot is ready")
    chat_logger.info("Bot is ready")


@bot.command(name="ping")
async def ping(ctx):
    """This is an example command, a nice and simple ping

    As seen in this example a command is declared as a function paired with a command decorator, do note that the
    decorator is your client object, this way you could theoretically have two clients written in the same file.
    The decorator has tons of features available to it, from things like aliasing commands to adding checks.

    For more details on command decorators:
    https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=command#discord.ext.commands.Command

    :param ctx: context, it would be a Message Object
    """
    await ctx.send('pong')


@bot.event
async def on_message(message):
    """Event fires whenever a message is sent to a guild the bot is in

    An event that fires every time a message is posted to a chat the bot is in, even pm chats. This event can be used to
    handle messages for the purposes of commands and chat logging. You can also hard code commands into this or even
    checks, but these are better handled via discord.py's implementation.
    It should be known that without this the bot would automatically run process_commands(message) for every message,
    after this is added the bot will no longer automatically run process_commands thus we have to call it.

    In this tutorial we will use this to handle chat logs.

    :param message: The Message object of the message sent
    """
    if message.author.id == bot.user.id:
        return
    global chat_logger
    chat_logger.info(f"{message.author}: {message.content}")
    await bot.process_commands(message)


if __name__ == "__main__":
    # The line of code that starts the bot thread, it should be noted that any code after this will not be executed
    bot.run(bot_cfg['token'])
