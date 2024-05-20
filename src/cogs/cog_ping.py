import discord
from discord.ext import commands
from time import time

from chat import Chat
from dotenv import dotenv_values


class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        config = dotenv_values('./.env')
        if config["GEMINI_API_KEY"] is None:
            raise ValueError("GEMINI_API_KEY is not found in .env file")
        self.chat_data = Chat(token=config["GEMINI_API_KEY"],
                              model=self.model_data.get_model_name(), default_prompt=self.model_data.get_prompt_default())

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Cog: ChatCog is ready!")

    @discord.app_commands.command(name="ping", description="BOTの生存確認を行い、応答速度を表示します。")
    async def command_ping(self, ctx: discord.interactions.Interaction) -> None:
        async with ctx.channel.typing():
            await ctx.response.defer(thinking=True)
            embed = discord.Embed(title=":ping_pong: pong!")
            embed.add_field(name=":globe_with_meridians: Discord WebSocket",
                            value=f"{round(self.bot.latency * 1000, 2)} ms", inline=True)
            embed.add_field(name=":link: Discord API Endpoint",
                            value=f"{round((time() - ctx.created_at.timestamp()) * 1000, 2)} ms", inline=True)
            embed.add_field(name=":speech_balloon: Gemini API",
                            value=str(self.chat_data.ping()), inline=False)
            await ctx.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCog(bot))
