import nextcord
from nextcord.ext import commands
import utils.json_loader as jl
from utils import checks
import inspect
import datetime
from collections import Counter
import asyncio
import os
import random
import traceback


class Owner(commands.Cog, name="Owner"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Toggle commands on or off."""
        command = self.bot.get_command(command)
        if command == None:
            await ctx.send("couldn't find that command ._.")
        elif ctx.command == command:
            await ctx.send('you can not disable this command._.')
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f'command {command.qualified_name} has been {ternary}')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, extension):
        if ctx.author.id == 741118153299591240:
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded")
            print(f"{extension} loaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @commands.command()
    @commands.is_owner()
    async def loadall(self, ctx):
        if ctx.author.id == 741118153299591240:
            for fn in os.listdir("./cogs"):
                if fn.endswith(".py"):
                    try:
                        bot.load_extension(f"cogs.{fn[:-3]}")
                        print(f'loaded {fn[:-3]}\n')
                    except Exception as error:
                        print(f'Failed to load extension {fn[:-3]}\n')
                await ctx.send("loaded extensions")
                print("loaded extensions")
        else:
            await ctx.send("Only bot devs can run this command")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension):
        if ctx.author.id == 741118153299591240:
            self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} reloaded")
            print(f"{extension} reloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, extension):
        if ctx.author.id == 741118153299591240:
            self.bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded")
            print(f"{extension} unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @commands.command()
    @commands.is_owner()
    async def check(self, ctx, *, extension):
        if ctx.author.id == 741118153299591240:
            try:
                self.bot.load_extension(f"cogs.{extension}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{extension} is loaded")
                print(f"{extension} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{extension} not found")
                print(f"{extension} not found")
            else:
                await ctx.send("{extension} is unloaded")
                self.bot.unload_extension(f"cogs.{extension}")
                print(f"{extension} is unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
