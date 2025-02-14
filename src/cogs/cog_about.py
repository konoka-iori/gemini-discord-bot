import logging

import discord
from discord.ext import commands

from json_load import jsonLoad


class GitHubLinkView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="GitHubでBOTのリポジトリを見る",
                url="https://github.com/konoka-iori/gemini-discord-bot",
                style=discord.ButtonStyle.url,
                emoji="🔗"
            )
        )


class AboutCog(commands.Cog):
    def __init__(self) -> None:
        self.command_data = jsonLoad()
        self.__logger = logging.getLogger("cog.about")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.__logger.info("Loaded Cog.")

    @discord.app_commands.command(name="about", description="BOTの説明を表示します。")
    async def command_about(self, ctx: discord.interactions.Interaction) -> None:
        await ctx.response.defer(thinking=True)
        try:
            embed_dict = self.command_data.get_command_embed("about")
            if embed_dict is None:
                self.__logger.error("embed_dict is None.")
                await ctx.followup.send("エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```/aboutのEmbedを取得できませんでした。```")
            else:
                await ctx.followup.send(embed=discord.Embed.from_dict(embed_dict), view=GitHubLinkView())
        except Exception as e:
            self.__logger.error(f"{e}")
            await ctx.followup.send(f"エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```{e}```")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AboutCog())
