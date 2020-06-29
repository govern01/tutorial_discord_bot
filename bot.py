from datetime import datetime
from configparser import ConfigParser
from discord.ext import commands

cfg = ConfigParser()
cfg.read("bot.ini")
bot_cfg = cfg['BOT']

bot = commands.Bot(command_prefix=bot_cfg['command_prefix'])


@bot.event
async def on_ready():
    cur = datetime.now()
    print(f"[{cur.strftime('%H:%M:%S')}] Bot is ready")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('pong')


@bot.event
async def on_message(message):
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(bot_cfg['token'])
