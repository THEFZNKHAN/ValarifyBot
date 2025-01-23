import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Intents
intents = discord.Intents.all()

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)


# Load cogs
async def load_cogs():
    try:
        await bot.load_extension("cogs.music")  # Use await for asynchronous cog loading
        print("Music cog loaded successfully.")
    except Exception as e:
        print(f"Failed to load Music cog: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready!")


# Async main function to run the bot
async def main():
    await load_cogs()  # Load cogs before starting the bot
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
