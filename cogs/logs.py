from nextcord.ext import commands, tasks
import nextcord
import datetime
import nextcord.errors
from nextcord.ext.commands import MissingPermissions

from utils.util import Pag
from nextcord.ext import commands
import nextcord.ext
from datetime import datetime

from nextcord import Embed
from nextcord.ext.commands import Cog
from nextcord.ext.commands import command



class Logs(commands.Cog, name="Logs"):
    """Logs"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        log_channel = self.bot.get_channel(903892893989732373)

    @Cog.listener()
    async def on_user_update(self, before, after):
        log_channel = self.bot.get_channel(903892893989732373)
        if before.name != after.name:
            embed = Embed(
                title="Username change",
                colour=after.colour,
                timestamp=datetime.now(),
            )

            fields = [("Before", before.name, False), ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(
                title="Discriminator change",
                colour=after.colour,
                timestamp=datetime.now(),
            )

            fields = [
                ("Before", before.discriminator, False),
                ("After", after.discriminator, False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

        if before.avatar.url != after.avatar.url:
            embed = Embed(
                title="Avatar change",
                description="New image is below, old to the right.",
                colour=after.colour,
                timestamp=datetime.now(),
            )

            embed.set_thumbnail(url=before.avatar.url)
            embed.set_image(url=after.avatar.url)

            await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = self.bot.get_channel(903892893989732373)
        if before.display_name != after.display_name:
            embed = Embed(
                title="Nickname change",
                colour=after.colour,
                timestamp=datetime.now(),
            )

            fields = [
                ("Before", before.display_name, False),
                ("After", after.display_name, False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(
                title="Role updates", colour=after.colour, timestamp=datetime.now()
            )

            fields = [
                ("Before", ", ".join([r.mention for r in before.roles]), False),
                ("After", ", ".join([r.mention for r in after.roles]), False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(903892893989732373)
        if not after.author.bot:
            if before.content != after.content:
                embed = Embed(
                    title="Message edit",
                    description=f"Edit by {after.author.display_name}.",
                    colour=after.author.colour,
                    timestamp=datetime.now(),
                )

                fields = [
                    ("Before", before.content, False),
                    ("After", after.content, False),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(903892893989732373)
        if not message.author.bot:
            embed = Embed(
                title="Message deletion",
                description=f"Action by {message.author.display_name}.",
                colour=message.author.colour,
                timestamp=datetime.now(),
            )

            fields = [("Content", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(Logs(bot))