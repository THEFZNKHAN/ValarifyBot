import os
import asyncio
import traceback

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import yt_dlp

from utils.queue import MusicQueue


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = MusicQueue()
        self.music_path = "./music"
        self.previous_songs = []

        os.makedirs(self.music_path, exist_ok=True)


    # *** Voice Channel Management Commands ***
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


    # *** Music Playback Commands ***
    @commands.command()
    async def play(self, ctx, url):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You need to be in a voice channel!")
                return

        self.music_queue.add_to_queue(ctx, url)
        await self.music_queue.play_next(ctx)

    @commands.command()
    async def clear(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I'm not connected to a voice channel.")
            return

        ctx.voice_client.stop()

        self.music_queue.clear()
        self.previous_songs.clear()

        await ctx.send("Stopped the music and cleared the queue.")

    @commands.command(aliases=["stop"])
    async def pause(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I'm not connected to a voice channel.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Music paused.")
        else:
            await ctx.send("No music is currently playing.")

    @commands.command()
    async def resume(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I'm not connected to a voice channel.")
            return

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Music resumed.")
        else:
            await ctx.send("No music is currently paused.")


    # *** Queue Management Commands ***
    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        if not self.music_queue.queue:
            await ctx.send("The queue is currently empty.")
            return

        queue_embed = discord.Embed(
            title="Current Music Queue", color=discord.Color.blue()
        )

        for i, (_, source) in enumerate(self.music_queue.queue, 1):
            try:
                with yt_dlp.YoutubeDL({"format": "bestaudio"}) as ydl:
                    info = (
                        ydl.extract_info(source, download=False)
                        if not os.path.exists(source)
                        else None
                    )
                    display_name = (
                        info.get("title", os.path.basename(source))
                        if info
                        else os.path.basename(source)
                    )
            except:
                display_name = os.path.basename(source)

            queue_embed.add_field(name=f"{i}. Song", value=display_name, inline=False)

        await ctx.send(embed=queue_embed)

    @commands.command(aliases=["skip"])
    async def next(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I'm not connected to a voice channel.")
            return

        ctx.voice_client.stop()

        if self.music_queue.queue:
            self.previous_songs.append(self.music_queue.queue[0])

        await self.music_queue.play_next(ctx)
        await ctx.send("Skipped to the next song.")

    @commands.command()
    async def previous(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I'm not connected to a voice channel.")
            return

        if not self.previous_songs:
            await ctx.send("No previous songs to go back to.")
            return

        ctx.voice_client.stop()

        previous_song = self.previous_songs.pop()
        self.music_queue.queue.insert(0, previous_song)

        await self.music_queue.play_next(ctx)
        await ctx.send("Playing the previous song.")


    # *** Audio Download and Playback Commands ***
    @commands.command()
    async def download_audio(self, ctx, url):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You need to be in a voice channel")
                return

        await ctx.send("Starting audio download...")

        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "outtmpl": os.path.join(self.music_path, "%(title)s.%(ext)s"),
            }

            def download_sync():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get("title", "Unknown")

                    ydl.download([url])

                    filename = ydl.prepare_filename(info)
                    filename = os.path.splitext(filename)[0] + ".mp3"
                    return title, os.path.basename(filename)

            title, filename = await asyncio.to_thread(download_sync)
            filepath = os.path.join(self.music_path, filename)
            self.music_queue.add_local_to_queue(ctx, filepath)  # Add to queue

            await self.music_queue.play_next(ctx)
            await ctx.send(f"Downloaded and queued: {title}")

        except Exception as e:
            await ctx.send(f"Download failed: {str(e)}")
            print(f"Download error: {traceback.format_exc()}")

    @commands.command()
    async def play_local(self, ctx, *filename_parts):
        if not ctx.voice_client:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                except Exception as connect_error:
                    await ctx.send(
                        f"Could not connect to voice channel: {connect_error}"
                    )
                    return
            else:
                await ctx.send("You must be in a voice channel!")
                return

        filename_query = " ".join(filename_parts)

        try:
            music_files = os.listdir(self.music_path)
            matching_files = [
                f
                for f in music_files
                if filename_query.lower() in f.lower()
                and f.lower().endswith((".mp3", ".wav"))
            ]
        except Exception as list_error:
            await ctx.send(f"Error accessing music directory: {list_error}")
            return

        if not matching_files:
            await ctx.send(f"No audio files found matching: {filename_query}")
            return

        filename = matching_files[0]
        filepath = os.path.join(self.music_path, filename)

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        try:
            source = FFmpegPCMAudio(filepath, **ffmpeg_options)
            ctx.voice_client.play(
                source,
                after=lambda e: print(
                    f"Playback finished. Error: {e}" if e else "Playback completed."
                ),
            )
            await ctx.send(f"Playing: {filename}")
        except Exception as play_error:
            await ctx.send(f"Error playing audio: {play_error}")


async def setup(bot):
    await bot.add_cog(Music(bot))
