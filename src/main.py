import os

import discord
from discord.ext import commands

from config import bot_prefix, BOT_TOKEN, SECRET
from web_server import start_web_server

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=bot_prefix, case_insensitive=True, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await load_commands()
    await bot.load_extension("error_handler")
    if SECRET:
        await start_web_server(bot)
    print("Bot ready.")


async def load_commands():
    for file in os.listdir("./commands"):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"commands.{file[:-3]}")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
