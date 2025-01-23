import os
import asyncio
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio


class MusicQueue:
    def __init__(self):
        self.queue = []
        self.is_playing = False

    def add_to_queue(self, ctx, url):
        self.queue.append((ctx, url))

    def add_local_to_queue(self, ctx, filepath):
        self.queue.append((ctx, filepath))

    async def play_next(self, ctx):
        if self.is_playing or len(self.queue) == 0:
            return

        self.is_playing = True
        current_ctx, source_info = self.queue[0]
        vc = current_ctx.voice_client

        try:
            if os.path.exists(source_info):
                FFMPEG_OPTIONS = {"options": "-vn"}
                source = FFmpegPCMAudio(source_info, **FFMPEG_OPTIONS)
                filename = os.path.basename(source_info)
                await current_ctx.send(f"Playing local file: {filename}")
            else:
                YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
                FFMPEG_OPTIONS = {"options": "-vn"}

                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(source_info, download=False)
                    url2 = info["url"]
                    source = FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
                    await current_ctx.send(f"Playing: {info['title']}")

            def after_playing(error):
                if error:
                    print(f"Player error: {error}")

                self.queue.pop(0)

                self.is_playing = False

                asyncio.run_coroutine_threadsafe(
                    self.play_next(current_ctx), current_ctx.bot.loop
                )

            vc.play(source, after=after_playing)

        except Exception as e:
            print(f"Error playing song: {e}")
            self.is_playing = False
            self.queue.pop(0)
            await current_ctx.send(f"Error playing song: {e}")

            await self.play_next(ctx)

    def clear(self):
        self.queue.clear()
        self.is_playing = False
