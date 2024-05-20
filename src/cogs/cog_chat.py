import discord
from discord.ext import commands
from json_load import ModelLoad
from chat import Chat
from dotenv import dotenv_values
from datetime import datetime


class ChatCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.model_data = ModelLoad()

        config = dotenv_values('./.env')
        if config["GEMINI_API_KEY"] is None:
            raise ValueError("GEMINI_API_KEY is not found in .env file")

        self.chat_data = Chat(token=config["GEMINI_API_KEY"],
                              model=self.model_data.get_model_name(), default_prompt=self.model_data.get_prompt_default())

    def generate_chat_embed(self, ctx: discord.interactions.Interaction, message: str) -> tuple[discord.Embed, discord.Embed]:
        """Generate Embeds to be used in chat commands.

        Args:
            ctx (discord.interactions.Interaction): Discord interaction context
            message (str): User message
        Returns:
            tuple[discord.Embed, discord.Embed]: [0]: User response embed, [1]: Gemini response embed
        """
        response = self.chat_data.get_response(message=message)
        user_embed = discord.Embed(
            description=message[:2048], color=discord.Color.green())
        user_embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
        user_embed.set_footer(text="User Prompt")
        user_embed.timestamp = ctx.created_at
        response_embed = discord.Embed(
            description=response[0][:2048], color=discord.Color.blue())
        response_embed.add_field(
            name="回答にかかった時間", value=f"{round(response[1], 2)} ms", inline=False)
        response_embed.set_author(
            name=self.model_data.get_name(), icon_url=self.model_data.get_icon())
        response_embed.set_footer(text=self.model_data.get_model_name())
        response_embed.timestamp = datetime.now()
        return user_embed, response_embed

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Cog: ChatCog is ready!")

    @discord.app_commands.command(name="chat", description="Gemini-Proと会話できます。")
    async def callback_chat(self, ctx: discord.interactions.Interaction, message: str) -> None:
        async with ctx.channel.typing():
            await ctx.response.defer(thinking=True)
            await ctx.followup.send(embeds=self.generate_chat_embed(ctx=ctx, message=message))

    # @discord.app_commands.context_menu(name="Gemini replies to message")
    # async def callback_reply(self, ctx: discord.interactions.Interaction, message: discord.Message) -> None:
    #     async with ctx.channel.typing():
    #         await ctx.response.defer(thinking=True)
    #         await ctx.followup.send(embeds=self.generate_chat_embed(ctx=ctx, message=message.content))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChatCog(bot))
