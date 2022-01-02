# Rebound Bot

# Imports
from discord.ext import commands
from discord import Intents
from os import getenv
from dotenv import load_dotenv

# Grab Token
load_dotenv()
TOKEN = getenv("TOKEN")
re = commands.Bot(command_prefix=">", intents=Intents.all())

# Bot Events
@re.event
async def on_ready():
    print("Connected to Discord!")

# On Some Joining
@re.event
async def on_member_join(member):
    with open("config", "r") as file:
        contents = file.read()
        contents = contents.split("\n")
    # Generate join message
    message = f"{member.mention} has joined us!"
    # Send it
    channel = re.get_channel(int(contents[3]))
    await channel.send(message)

# On Some Leaving
@re.event
async def on_member_remove(member):
    with open("config", "r") as file:
        contents = file.read()
        contents = contents.split("\n")
    # Generate join message
    message = f"{member.mention} has left us!"
    # Send it
    channel = re.get_channel(int(contents[4]))
    await channel.send(message)
    


# Announcement Command
@re.command(name="announce", aliases=["a"])
async def announce(ctx):
    await publish(ctx, 0)

# Devlog Command
@re.command(name="devlog", aliases=["dv"])
async def devlog(ctx):
    await publish(ctx, 1)

# Publish (Announcement) Command
async def publish(ctx, channel):
    with open("config", "r") as file:
        contents = file.read()
        contents = contents.split("\n")

    # Check if admin
    role_id = int(contents[2])
    author_roles = [role.id for role in ctx.author.roles]
    if not role_id in author_roles:
        await ctx.message.delete()
        return

    # Check if a response
    if not ctx.message.reference:
        await ctx.send("Reply to the message you want to announce!")
        return

    # Grab channel
    announcement_channel = int(contents[channel])
    channel = re.get_channel(announcement_channel)

    # Send message with OG message content
    ctx = await ctx.fetch_message(id=ctx.message.reference.message_id)
    await channel.send(f"@everyone {ctx.content}")


# Run Code
if __name__ == "__main__":
    re.run(TOKEN)