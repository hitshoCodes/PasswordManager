import discord
from discord.ext import commands
import json
from password_manager import view_pass, add_pass, remove_pass, check_pass_strength, authenticate_user

# Load settings from settings.json
def load_settings():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    return settings

settings = load_settings()
DISCORD_TOKEN = settings["discord_token"]
YOUR_ID = settings["your_id"]

bot = commands.Bot(command_prefix="!")  # Change the prefix as desired

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="view")
async def view(ctx):
    if str(ctx.author.id) == YOUR_ID:
        view_pass(key)  # Note: 'key' should be set from authenticate_user() in password_manager.py
    else:
        await ctx.send("You are not authorized to use this command.")

@bot.command(name="add")
async def add(ctx):
    if str(ctx.author.id) == YOUR_ID:
        add_pass(key)  # Note: 'key' should be set from authenticate_user() in password_manager.py
        await ctx.send("Password added successfully!")
    else:
        await ctx.send("You are not authorized to use this command.")

@bot.command(name="remove")
async def remove(ctx, index: int):
    if str(ctx.author.id) == YOUR_ID:
        remove_pass(index)
        await ctx.send("Password removed successfully!")
    else:
        await ctx.send("You are not authorized to use this command.")

@bot.command(name="check")
async def check(ctx, *, passw: str):
    if str(ctx.author.id) == YOUR_ID:
        check_pass_strength(passw)
    else:
        await ctx.send("You are not authorized to use this command.")

key = authenticate_user()
if key is None:
    exit()

bot.run(DISCORD_TOKEN)
