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

    @commands.command(name="list")
    @commands.guild_only()
    @commands.is_owner()
    async def list_extensions(self, ctx):
        list = nextcord.Embed(title="Extensions List", description="1.blacklist\n2.block\n3.channel\n4.economy\n5.info\n6.infractions\n7.instructions\n8.misc\n9.moderation\n10.profanity\n11.rtfm\n12.support\n13.tickets")
        await ctx.send(embed=list)

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

    @commands.command(
        aliases=["giverole", "addr"], description="Gives a member a certain role."
    )
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a user to give them a role!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a role to give {} that role!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Add Role Error",
                description="You do not have enough permissions to give this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = nextcord.Embed(
                    title="Add Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Add Role Success",
                    description=f"{role.mention} has been assigned to {member.mention}",
                )
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)

    @commands.command(
        aliases=["takerole", "remover"],
        description="Removes a certain role from a member.",
    )
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx,
        member: nextcord.Member = None,
        role: nextcord.Role = None,
        *,
        reason=None,
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a user to remove a role from them!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a role to remove the role from {}!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Remove Role Error",
                description="You do not have enough permissions to remove this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            roleRemoved = False
            for role_ in member.roles:
                if role_ == role:
                    await member.remove_roles(role)
                    roleRemoved = True
                    break
            if not roleRemoved:
                embed = nextcord.Embed(
                    title="Remove Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Remove Role Success!",
                    description=f"{role.mention} has been removed from {member.mention}",
                )
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
