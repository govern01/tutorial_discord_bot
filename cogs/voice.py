from discord.ext import commands
from discord.utils import get
import discord
import os

MP3FILEPATH = "./voice_files/"


class VoiceCog(commands.Cog, name="Voice Chat"):
    def __init__(self, bot):
        self.bot = bot

    """
    Whenever a join occurs a VoiceClient is created, voice_client objects are returned however discord.py will natively
    keep track of all VoiceClients via the bot object, there can only exist one voice_client per server therefor we can
    use the discord.utils get command to find the voice_client associated with our guild, if any.
    Do note the bot connects to a channel via the VoiceChannel object.
    """
    @commands.guild_only()
    @commands.command(name="join")
    async def join_voice(self, ctx):
        channel = ctx.message.author.voice.channel
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            await channel.connect()

    """
    Unlike the method of connecting, disconnect occurs with the VoiceClient.
    """
    @commands.guild_only()
    @commands.command(name="leave")
    async def leave_voice(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        await voice_client.disconnect()

    """
    The play function takes any AudioSource or AudioSource derivative as a param to play from, there are many native
    types in discord.py all of which can be found in the docs. using FFmpeg requires the library to exist in your path
    variables.
    """
    @commands.guild_only()
    @commands.command(name="play")
    async def play(self, ctx, filename: str):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        voice_client.play(discord.FFmpegPCMAudio(f"{MP3FILEPATH}{filename}.mp3"))

    """
    Below are three simple commands to change how the bot is streaming audio.
    """
    @commands.guild_only()
    @commands.command(name="pause")
    async def pause(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        voice_client.pause()

    @commands.guild_only()
    @commands.command(name="resume")
    async def resume(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        voice_client.resume()

    @commands.guild_only()
    @commands.command(name="stop")
    async def stop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        voice_client.stop()


def setup(bot):
    if not os.path.isdir(MP3FILEPATH):
        os.mkdir(MP3FILEPATH)
    bot.add_cog(VoiceCog(bot))
