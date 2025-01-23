import asyncio
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio


class MusicQueue:
    def __init__(self):
        self.queue = []

    def add_to_queue(self, ctx, url):
        self.queue.append((ctx, url))

    async def play_next(self, ctx):
        if len(self.queue) > 0:
            current_ctx, url = self.queue[0]

            YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
            FFMPEG_OPTIONS = {"options": "-vn"}
            vc = current_ctx.voice_client

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info["url"]
                source = FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
                vc.play(
                    source,
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_next(ctx), current_ctx.bot.loop
                    ),
                )

            await ctx.send(f"Playing: {info['title']}")
            self.queue.pop(0)

    def clear(self):
        self.queue.clear()
