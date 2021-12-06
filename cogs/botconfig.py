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
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        '''Ändert das derzeit spielende Spiel (BOT OWNER ONLY)'''
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
        await ctx.send(f'**:ok:** Ändere das Spiel zu: {gameType} **{gameName}**')

    @commands.command()
    async def changestatus(self, ctx, status: str):
        '''Ändert den Online Status vom Bot (BOT OWNER ONLY)'''
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
        await ctx.send(f'**:ok:** Ändere Status zu: **{nextcordStatus}**')

    @commands.command(aliases=['guilds'])
    async def servers(self, ctx):
        '''Listet die aktuellen verbundenen Guilds auf (BOT OWNER ONLY)'''
        msg = '```py\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.command()
    async def leaveserver(self, ctx, guildid: str):
        '''Tritt aus einem Server aus (BOT OWNER ONLY)
        Beispiel:
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
                msg = f':ok: Austritt aus {guild.name} erfolgreich!'
            else:
                msg = ':x: Konnte keine passende Guild zu dieser ID finden!'
        await ctx.send(msg)

    @commands.command()
    async def discriminator(self, ctx, disc: str):
        '''Gibt Benutzer mit dem jeweiligen Discriminator zurück'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(':x: Konnte niemanden finden')

    @commands.command()
    @commands.bot_has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, *name):
        '''Ändert den Server Nickname vom Bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Ändere meinen Server Nickname zu: **{nickname}**'
        else:
            msg = f':ok: Reset von meinem Server Nickname auf: **{ctx.me.name}**'
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

def setup(bot: commands.Bot):
    bot.add_cog(Botconfig(bot))
