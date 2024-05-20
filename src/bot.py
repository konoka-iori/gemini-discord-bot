from os import listdir

import asyncio

import discord
import discord.app_commands
from discord.ext import commands
from dotenv import dotenv_values


async def main() -> None:
    """.envファイルから設定を読み込み、ボットを初期化して起動します。"""

    config = dotenv_values('./.env')  # .envファイルを読み込む
    # .envファイルの検証
    if config["DISCORD_BOT_TOKEN"] is None:
        raise ValueError("DISCORD_BOT_TOKEN is not found in .env file")
    if config["DISCORD_SERVER_ID"] is None:
        raise ValueError("DISCORD_SERVER_ID is not found in .env file")

    # .envファイルから取得した値を変数に代入
    DISCORD_BOT_TOKEN = config["DISCORD_BOT_TOKEN"]
    GEMINI_API_KEY = config["GEMINI_API_KEY"]
    DISCORD_SERVER_ID = discord.Object(id=int(config["DISCORD_SERVER_ID"]))

    # Botを作成
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

    @bot.event
    async def setup_hook() -> None:  # on_readyの前に実行されるイベントリスナー
        await bot.tree.sync()  # グローバルコマンドを同期する
        print("GLOBAL COMMANDS SYNCED")
        await bot.tree.sync(guild=DISCORD_SERVER_ID)  # ギルドにコマンドを同期する
        print("COMMANDS SYNCED")

    @bot.event
    async def on_ready() -> None:  # Botが起動したときに実行されるイベントリスナー
        print(f"LOGGED IN: {bot.user.name}")

    asyncio.gather(*[bot.load_extension(f"cogs.{cog[:-3]}")
                   for cog in listdir("src/cogs") if cog.endswith(".py")])
    await bot.start(DISCORD_BOT_TOKEN)  # Botを起動


if __name__ == "__main__":
    asyncio.run(main())

# @client.event
# async def on_ready() -> None:
#     await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="Gemini 1.5 Proを実行中"))
#     print("PRESENCE UPDATED")
#     print(model_data.get_prompt_default())
