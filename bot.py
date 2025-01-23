import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()

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


async def main():
    await load_cogs()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
