import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs():
    try:
        await bot.load_extension("cogs.music")
        print("Music cog loaded successfully.")
    except Exception as e:
        print(f"Failed to load Music cog: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready!")
    print(f"Bot is connected to {len(bot.guilds)} guilds")


async def main():
    await load_cogs()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
