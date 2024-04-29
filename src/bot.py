from os import getenv
from time import time
import discord
import discord.app_commands
import chat
import json_load


DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")
DISCORD_SERVER_ID = discord.Object(getenv("DISCORD_SERVER_ID"))

command_data = json_load.jsonLoad()
model_data = json_load.ModelLoad()
chat_data = chat.Chat(token=GEMINI_API_KEY, model=model_data.get_model_name())


client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)


def generate_chat_embed(ctx:discord.Integration, message:str) -> tuple[discord.Embed, discord.Embed]:
    response = chat_data.get_response(message)
    user_embed = discord.Embed(description=message[:2048], color=discord.Color.green())
    user_embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
    response_embed = discord.Embed(description=response[0][:2048], color=discord.Color.blue())
    response_embed.add_field(name="回答にかかった時間", value=f"{round(response[1], 2)} ms", inline=False)
    response_embed.set_author(name=model_data.get_name(), icon_url=model_data.get_icon())
    return user_embed, response_embed


@tree.command(name="about", description=command_data.get_command_description("about"))
async def command_about(ctx:discord.Interaction) -> None:
    async with ctx.channel.typing():
        await ctx.response.defer(thinking=True)
        await ctx.followup.send(embed=discord.Embed.from_dict(command_data.get_command_embed("about")))

@tree.command(name="ping", description=command_data.get_command_description("ping"))
async def command_ping(ctx:discord.Interaction) -> None:
    async with ctx.channel.typing():
        await ctx.response.defer(thinking=True)
        embed = discord.Embed(title=":ping_pong: pong!")
        embed.add_field(name=":globe_with_meridians: Discord WebSocket", value=f"{round(client.latency, 2)} ms", inline=True)
        embed.add_field(name=":link: Discord API Endpoint", value=f"{round(time() - ctx.created_at.timestamp(), 2)} ms", inline=True)
        embed.add_field(name=":speech_balloon: Gemini API", value=str(chat_data.ping()), inline=False)
        await ctx.followup.send(embed=embed)

@tree.command(name="chat", description=command_data.get_command_description("chat"))
async def command_chat(ctx:discord.Interaction, message:str) -> None:
    async with ctx.channel.typing():
        await ctx.response.defer(thinking=True)
        await ctx.followup.send(embeds=generate_chat_embed(ctx, message))

@tree.context_menu(name="Gemini replies to message")
async def command_reply(ctx:discord.Interaction, message:discord.Message) -> None:
    async with ctx.channel.typing():
        await ctx.response.defer(thinking=True)
        await ctx.followup.send(embeds=generate_chat_embed(ctx, message.content))


@client.event
async def on_ready() -> None:
    print(f"LOGGED IN: {client.user.name}")
    tree.copy_global_to(guild=DISCORD_SERVER_ID)
    await tree.sync(guild=DISCORD_SERVER_ID) # コマンドを同期
    print("COMMAND SYNCED")
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="Gemini 1.5 Proを実行中"))
    print("PRESENCE UPDATED")


# Discordに接続
client.run(DISCORD_BOT_TOKEN)
