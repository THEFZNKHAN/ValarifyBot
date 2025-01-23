import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
import subprocess
from utils.queue import MusicQueue


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = MusicQueue()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            permissions = channel.permissions_for(ctx.guild.me)
            if permissions.connect:
                await channel.connect()
            else:
                await ctx.send("I don't have permission to join the voice channel.")
            await ctx.send(f"Joined {channel}")
        else:
            await ctx.send("You need to join a voice channel first!")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel!")

    @commands.command()
    async def play(self, ctx, url):
        if not ctx.voice_client:
            await ctx.send("I'm not in a voice channel. Use !join first.")
            return

        # Add song to queue
        self.music_queue.add_to_queue(ctx, url)
        if len(self.music_queue.queue) == 1:
            await self.music_queue.play_next(ctx)

    @commands.command()
    async def play_local(self, ctx, filename: str):
        vc = ctx.voice_client
        if not vc:
            await ctx.send("I'm not in a voice channel. Use !join first.")
            return

        filepath = f"./music/{filename}.mp3"
        if not os.path.exists(filepath):
            await ctx.send("File not found!")
            return

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug",
            "options": "-vn",
        }

        try:
            source = FFmpegPCMAudio(filepath, **ffmpeg_options)
            vc.play(source)
            await ctx.send(f"Playing: {filename}")
        except Exception as e:
            await ctx.send("Failed to play audio!")
            print(f"Error: {e}")

    @commands.command()
    async def test_audio(self, ctx):
        vc = ctx.voice_client
        if not vc:
            await ctx.send("I'm not in a voice channel. Use !join first.")
            return

        try:
            vc.play(
                discord.FFmpegPCMAudio(
                    "anullsrc=r=44100:cl=stereo",
                    before_options="-f lavfi",
                    options="-t 10",
                )
            )
            await ctx.send("Playing test tone...")
        except Exception as e:
            await ctx.send("Failed to play test audio!")
            print(f"Error: {e}")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            self.music_queue.clear()
            await ctx.send("Music stopped.")
        else:
            await ctx.send("No music is playing.")


async def setup(bot):
    await bot.add_cog(Music(bot))
