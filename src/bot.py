import asyncio
from os import listdir

import discord
import discord.app_commands
from discord.ext import commands
from dotenv import dotenv_values


async def main() -> None:
    """.envファイルから設定を読み込み、BOTを初期化して起動します。"""

    config = dotenv_values('./.env')
    DISCORD_BOT_TOKEN = config.get("DISCORD_BOT_TOKEN")
    GEMINI_API_KEY = config.get("GEMINI_API_KEY")
    DISCORD_SERVER_ID = config.get("DISCORD_SERVER_ID")

    if DISCORD_BOT_TOKEN is None:
        raise ValueError("DISCORD_BOT_TOKEN is not found in .env file")
    if GEMINI_API_KEY is None:
        raise ValueError("GEMINI_API_KEY is not found in .env file")
    if DISCORD_SERVER_ID is None:
        raise ValueError("DISCORD_SERVER_ID is not found in .env file")

    DISCORD_SERVER = discord.Object(id=int(DISCORD_SERVER_ID))

    # Botを作成
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())
    bot.gemini_api_key = GEMINI_API_KEY  # NOTE:この方法どうなのかな？もっと良い方法があれば変えたい。

    @bot.event
    async def setup_hook() -> None:
        await bot.tree.sync()  # グローバルコマンドを同期する
        print("GLOBAL COMMANDS SYNCED")
        await bot.tree.sync(guild=DISCORD_SERVER)  # ギルドにコマンドを同期する
        print("COMMANDS SYNCED")

    @bot.event
    async def on_ready() -> None:
        print(f"LOGGED IN: {bot.user.name}")
        await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="Gemini 1.5 Proを実行中"))
        print("PRESENCE UPDATED")

    asyncio.gather(*[bot.load_extension(f"cogs.{cog[:-3]}")
                   for cog in listdir("src/cogs") if cog.endswith(".py")])
    await bot.start(DISCORD_BOT_TOKEN)  # Botを起動


if __name__ == "__main__":
    asyncio.run(main())
