import discord
from discord.ext import commands

from json_load import jsonLoad


class GitHubLinkView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(discord.ui.Button(label="GitHubでBOTのリポジトリを見る",
                      url="https://github.com/konoka-iori/gemini-discord-bot", style=discord.ButtonStyle.url, emoji="🔗"))


class AboutCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.command_data = jsonLoad()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Cog: AboutCog is ready!")

    @discord.app_commands.command(name="about", description="BOTの説明を表示します。")
    async def command_about(self, ctx: discord.interactions.Interaction) -> None:
        async with ctx.channel.typing():
            await ctx.response.defer(thinking=True)
            await ctx.followup.send(embed=discord.Embed.from_dict(self.command_data.get_command_embed("about")), view=GitHubLinkView())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AboutCog(bot))
