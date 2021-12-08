"""
Help Cog with button component pagination by Jonah Lawrence (DenverCoder1)

The basic embed help command is based on this gist by Rapptz
https://gist.github.com/Rapptz/31a346ed1eb545ddeb0d451d81a60b3b
"""

from dataclasses import dataclass
from typing import List

import config
import nextcord
from nextcord.ext import commands, menus

@dataclass
class EmbedField:
    name: str
    value: str
    inline: bool

class HelpPages(menus.ListPageSource):
    def __init__(self, help_command: "NewHelpCommand", data: List[EmbedField]):
        self._help_command = help_command
        super().__init__(data, per_page=4)
        
    async def format_page(self, menu: menus.Menu, entries: List[EmbedField]) -> nextcord.Embed:
        invoked_with = self._help_command.invoked_with
        embed = nextcord.Embed(title="__Bot Commands__",
                               colour=self._help_command.COLOUR)
        embed.description = (
            f'Use "<Prefix> help <command>" for more info on a command.\n'
            f'Use "<Prefix> help <category>" for more info on a category.'
        )
        for entry in entries:
            embed.add_field(
                name=entry.name, value=entry.value, inline=entry.inline
            )
        embed.set_footer(
            text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class NewHelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds"""

    # embed colour
    COLOUR = nextcord.Colour.blurple()

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        prefix = config.PREFIX
        return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        prefix = config.PREFIX
        invoked_with = self.invoked_with
        embed = nextcord.Embed(title="__Bot Commands__", colour=self.COLOUR)
        embed.description = (
            f'Use "<Prefix> help <command>" for more info on a command.\n'
            f'Use "<Prefix> help <category>" for more info on a category.'
        )

        embed_fields: List[EmbedField] = []

        for cog, commands in mapping.items():
            name = "__**No Category**__" if cog is None else (
                f"__**{cog.qualified_name}**__")
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # \u2002 = en space
                value = "\u2002".join(f"`{c.name}`" for c in filtered)
                if cog and cog.description:
                    value = f"{value}"
                embed_fields.append(
                    EmbedField(name=name, value=value, inline=False)
                )

        pages = menus.ButtonMenuPages(
            source=HelpPages(self, embed_fields),
            clear_buttons_after=True,
            style=nextcord.ButtonStyle.primary
        )
        await pages.start(self.context)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        embed = nextcord.Embed(
            title=f"{cog.qualified_name} Commands", colour=self.COLOUR
        )
        if cog.description:
            embed.description = (f"{cog.description}")

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=self.get_command_signature(command),
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(
            text=f"Use <Prefix> help [command] for more info on a command.")
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        """implements group help page and command help page"""
        embed = nextcord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False,
                )

        await self.get_destination().send(embed=embed)

    # Use the same function as group help for command help
    send_command_help = send_group_help
