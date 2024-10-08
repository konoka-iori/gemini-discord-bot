import asyncio
import logging
import logging.handlers
from datetime import datetime
from os import listdir, makedirs, path

import discord
import discord.app_commands
from discord.ext import commands
from dotenv import dotenv_values


async def main() -> None:
    """.envファイルから設定を読み込み、BOTを初期化して起動します。"""

    config = dotenv_values("./.env")
    DISCORD_BOT_TOKEN = config.get("DISCORD_BOT_TOKEN")
    GEMINI_API_KEY = config.get("GEMINI_API_KEY")

    if DISCORD_BOT_TOKEN is None:
        raise ValueError("DISCORD_BOT_TOKEN is not found in .env file")
    if GEMINI_API_KEY is None:
        raise ValueError("GEMINI_API_KEY is not found in .env file")

    # ログの設定
    LOG_DIR = "log/"
    if not path.exists(LOG_DIR): # logディレクトリがないときに作成
        makedirs(LOG_DIR)
    handler = logging.handlers.RotatingFileHandler(
        filename=f"{LOG_DIR}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        encoding="utf-8",
        mode="w",
    )
    logging.basicConfig(level=logging.INFO, handlers=[handler],
                        format="{asctime} {levelname} {name}: {message}",
                        style="{", datefmt="%Y-%m-%d %H:%M:%S")

    # ロガーの定義
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)

    # Botを作成
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())
    bot.gemini_api_key = GEMINI_API_KEY  # NOTE:この方法どうなのかな？もっと良い方法があれば変えたい。

    @bot.event
    async def setup_hook() -> None:
        await bot.tree.sync()  # グローバルコマンドを同期する
        logger.info("GLOBAL COMMANDS SYNCED.")

    @bot.event
    async def on_ready() -> None:
        logger.info(f"LOGGED IN -> {bot.user.name}")
        await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="Gemini 1.5 Proを実行中"))
        logger.info("PRESENCE UPDATED.")
        print(f"LOGGED IN: {bot.user.name}")

    asyncio.gather(*[bot.load_extension(f"cogs.{cog[:-3]}")
                   for cog in listdir("src/cogs") if cog.endswith(".py")])
    await bot.start(DISCORD_BOT_TOKEN)  # Botを起動


if __name__ == "__main__":
    asyncio.run(main())
