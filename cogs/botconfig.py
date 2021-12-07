import math
import aiosqlite
import asyncio
import nextcord
from nextcord.ext import commands
import sys
import os
import random
import aiohttp
# should be fixed

class Botconfig(commands.Cog, name="Botconfig"):
    """Bot Config commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(aliases=['game'])
    @commands.has_role('Bot Manager')
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        '''Changes the game currently playing (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            activityType = nextcord.ActivityType.playing
        elif gameType == 'watching':
            activityType = nextcord.ActivityType.watching
        elif gameType == 'listening':
            activityType = nextcord.ActivityType.listening
        elif gameType == 'streaming':
            activityType = nextcord.ActivityType.streaming
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(activity=nextcord.Activity(type=activityType, name=gameName))
        await ctx.send(f'**:ok:** Change the game to: {gameType} ** {gameName} **')

    @commands.command()
    @commands.has_role('Bot Manager')
    async def changestatus(self, ctx, status: str):
        '''Changes the online status of the bot (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            nextcordStatus = nextcord.Status.invisible
        elif status == 'idle':
            nextcordStatus = nextcord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            nextcordStatus = nextcord.Status.dnd
        else:
            nextcordStatus = nextcord.Status.online
        await self.bot.change_presence(status=nextcordStatus)
        await ctx.send(f'**:ok:** Change status to: **{nextcordStatus}**')

    @commands.command(aliases=['guilds'])
    @commands.has_role('Bot Manager')
    async def servers(self, ctx):
        '''Lists the current connected guilds (BOT OWNER ONLY)'''
        msg = '```py\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.command()
    @commands.is_owner()
    async def leaveserver(self, ctx, guildid: str):
        '''Exits a server (BOT OWNER ONLY)
        Example:
        -----------
        :leaveserver 102817255661772800
        '''
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f':ok: Successful exit from {guild.name}!'
            else:
                msg = ":x: Couldn't find a suitable guild for this ID!"
        await ctx.send(msg)

    @commands.command()
    @commands.has_role('Bot Manager')
    async def discriminator(self, ctx, disc: str):
        '''Returns users with the respective discriminator'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(":x: Couldn't find anyone")

    @commands.command()
    @commands.has_role('Bot Manager')
    async def nickname(self, ctx, *name):
        '''Changes the server nickname of the bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f'Changed my server nickname to: **{nickname}**'
        else:
            msg = f'Reset my server nickname on: **{ctx.me.name}**'
        await ctx.send(msg)

    """@commands.command()
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, member: nextcord.Member=None, *name):
        '''Ändert den Nickname eines Benutzer (BOT OWNER ONLY)'''
        if member == None:
            member = ctx.author
        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f':ok: Ändere Nickname von {member} zu: **{nickname}**'
        else:
            msg = f':ok: Reset von Nickname für {member} auf: **{member.name}**'
        await ctx.send(msg)

    @commands.command()
    async def name(self, ctx, name: str):
        '''Ändert den globalen Namen vom Bot (BOT OWNER ONLY)'''
        await self.bot.edit_profile(username=name)
        msg = f':ok: Ändere meinen Namen zu: **{name}**'
        await ctx.send(msg)

    @commands.command()
    async def geninvite(self, ctx, serverid: str):
        '''Generiert einen Invite für eine Guild wenn möglich (BOT OWNER ONLY)'''
        guild = self.bot.get_guild(int(serverid))
        invite = await self.bot.create_invite(guild, max_uses=1, unique=False)
        msg = f'Invite für **{guild.name}** ({guild.id})\n{invite.url}'
        await ctx.author.send(msg)"""

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
        list = nextcord.Embed(title="Extensions List", description="1.economy\n2.info\n3.infractions\n4.instructions\n5.misc\n6.support\n7.tickets\n8.leveling")
        await ctx.send(embed=list)



def setup(bot: commands.Bot):
    bot.add_cog(Botconfig(bot))
