from os import getenv
import discord
import discord.app_commands
import chat
import json_load


DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")
DISCORD_SERVER_ID = discord.Object(getenv("DISCORD_SERVER_ID"))

command_data = json_load.jsonLoad()
chat_data = chat.Chat(GEMINI_API_KEY)


client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)


@tree.command(name="about", description=command_data.get_command_description("about"), guild=DISCORD_SERVER_ID)
async def about(ctx:discord.Interaction) -> None:
    async with ctx.channel.typing():
        await ctx.response.defer(thinking=True)
        embed = discord.Embed.from_dict(command_data.get_command_embed("about"))
        await ctx.followup.send(embed=embed)

@tree.command(name="chat", description=command_data.get_command_description("chat"), guild=DISCORD_SERVER_ID)
async def chat(ctx:discord.Interaction, message:str) -> None:
    async with ctx.channel.typing():
        await ctx.response.defer(thinking=True)
<<<<<<< HEAD
        await ctx.followup.send(chat_data.get_response(message))

# BUG:ctx.message.reference.resolved.contentがNoneになる
# @tree.command(name="reply", description=command_data.get_command_description("reply"), guild=DISCORD_SERVER_ID)
# async def reply(ctx:discord.Interaction) -> None:
#     async with ctx.channel.typing():
#         await ctx.response.defer(thinking=True)
#         await ctx.followup.send(chat_data.get_response(ctx.message.reference.resolved.content))

=======
        embed = discord.Embed(description=message)
        embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
        embed.add_field(name="Gemini-Proの回答", value=chat_data.get_response(message)[:1024])
        await ctx.followup.send(embed=embed)
>>>>>>> 266fe02b63188aba1a14e18fdbb70f05606d1974

@client.event
async def on_ready() -> None:
    print("LOGGED IN")
    await tree.sync(guild=DISCORD_SERVER_ID) #コマンド同期
    print("COMMAND SYNCED")


# Discordに接続
client.run(DISCORD_BOT_TOKEN)