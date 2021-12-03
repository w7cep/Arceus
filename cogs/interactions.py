import config
import nextcord
import datetime
from nextcord.ext import commands

from util.confirm_view import ConfirmView
from util.self_role_view import SelfRoleView
from util.sysbot_role_view import SysBotRuleView
from util.dropdown_view import DropdownView
from util.color_role_view import ColorRoleView


class Interactions(commands.Cog, name="Interactions"):
    """Server Suggestion Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When the bot is ready, load the role views"""
        # skip this function if views are already added
        if self.__bot.persistent_views_added:
            return
        self.__bot.add_view(SelfRoleView())
        self.__bot.add_view(ConfirmView())
        self.__bot.add_view(SysBotRuleView())
        self.__bot.add_view(ColorRoleView())
        # set flag
        self.__bot.persistent_views_added = True
        print("Button views added")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.is_owner()
    async def view(self, ctx):
        """Role Views"""
        await ctx.send("Invalid sub-command specified")

    @view.command(name="sysbot_roles")
    @commands.is_owner()
    async def sysbot_roles(self, ctx: commands.Context, message_id: str):
        """Starts a bot role view aka bot access role"""
        bot_rules_channel = await ctx.guild.fetch_channel(config.BOT_RULES_CHANNEL_ID)
        message = await bot_rules_channel.fetch_message(message_id)
        await message.edit(view=SysBotRuleView())

    @view.command(name="add_confirm")
    @commands.is_owner()
    async def add_confirm(self, ctx: commands.Context, message_id: str):
        """Starts a confirm view aka default role button"""
        rules_channel = await ctx.guild.fetch_channel(config.RULES_CHANNEL_ID)
        message = await rules_channel.fetch_message(message_id)
        await message.edit(view=ConfirmView())

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.is_owner()
    async def access(self, ctx):
        """Access commands"""
        await ctx.send("Invalid sub-command specified")

    @access.command(name="server_rules")
    @commands.is_owner()
    @commands.guild_only()
    async def server_rules(self, ctx):
        """Server Rules. with reaction role"""
        embed = nextcord.Embed(
            title="__**Frogadier's Grotto Rules**__",
            description=f"\n<:Switch:865465921040678932> __**The Rules**__ <:Switch:865465921040678932>\n\n"
            f"1. Full compliance to Discord's ToS.\n"
            f"2. Absolutely no drama.\n"
            f"3. Got issues with someone, talk to <@&829942684947841024>  or <@&867254914563178527> or resolve it in DM's.\n"
            f"4. Keep your -isms IRL and not in here.\n"
            f"5. You've got 3 strikes, so don't be that person.\n"
            f"6. Invite your friends, yet keep the Drama Queens out.\n"
            f"7. Please keep Politics and Religion out, we don't mind a healthy discussion, but DMs are best suited for that.\n"
            f"8. We allow pinging each other, demanding not to get pinged will get you a warning.\n"
            f"9. We don't mind cussing, sarcasm or sexually tinted jokes, but keep porn out.\n"
            f"10. Don't ask or distribute illegal Pokémon, talk is permitted (Use `!illegal` for a list).\n"
            f"11. No selling of any kind. (unless approved by an admin).\n"
            f"12. Don't DM other members unless you have their permission to do so.\n\n"
            f"This can be updated for future reference.\n\n"
            f"Click :thumbsup:Confirm to gain access to the rest of the server!\n\n"
            f"Then visit <#861616591199141908> to give yourself some roles and <#868914000572846120> for Sys-Bot access!\n\n"
            f"https://discord.gg/dm7gSAT68d\n\n"
            f"Server and Bot rules subject to change.\n\n"
            f"<a:rainbowmeltandab:866027057691230229>\n\n"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_author(
            name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        embed.set_footer(text="Bot is running v1.0.0")
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed, view=ConfirmView())

    @access.command(name="sysbot_rules")
    @commands.is_owner()
    @commands.guild_only()
    async def sysbot_rules(self, ctx):
        """SysBot Rules. with reaction role"""
        version = "v1.1.0"

        embed = nextcord.Embed(
            title="__**Greninja SysBot Rules**__",
            description="Anyone who break the rules or is just straight up a pain in the ass about it, gets access revoked, to either the bot or the server. \n\n1. Don't try anything illegal, it won't work. \n2. You've tried everything and it still isn't legal, DM or ping <@&858153204146634782> \n2. Help can be asked, we won't shy away from it just make sure you've read<#858130122221420554> first. \n3. Anyone who uses it, does so at their own discretion. Don't be that person to call others out for using it. \n4. First try? Checkout <#858130122221420554> \n5. Made anything with the bot and you go sell it, insta-ban, no excuses.\n6. Refrain from deleting messages, even if it's a spelling mistake.  \n8. Have fun and Be respectful\n9. Using the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n10. No code sharing. The bot is for this server only\n\nBot access will be revoked for multiple offenders.\n\nRequests for special mons can be made in <#865074053759893525> , The PK8 Master will get to it as soon as he can.\n\nTo get access to the bots click below!\n🤖: Greninja SysBot Access",
            colour=nextcord.Colour.blue()
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_author(
            name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"Bot is running {version}")
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed, view=SysBotRuleView())

    @access.command(name="get_roles")
    @commands.is_owner()
    async def get_roles(self, ctx: commands.Context):
        """Starts a access role view"""
        embed = nextcord.Embed(
            title="__**Access Roles**__",
            description="Click on a button to select a role"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_author(
            name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        embed.set_footer(text="Bot is running v1.0.0")
        embed.add_field(name="__*General Access*__", value=f"**Giveaway Access**: 🎉\n"
                        f"**TradeCord Channel Access**: 🌀", inline=False)
        embed.add_field(name="__*Misc Roles*__", value=f"**Sword**: ⚔\n"
                        f"**Shield**: 🛡", inline=False)
        embed.add_field(name="__*Gender Roles*__", value=f"**Female**: 🚺\n"
                        f"**Male**: 🚹\n"
                        f"**Other**: 🚻", inline=False)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed, view=SelfRoleView())

    @access.command(name="color_roles")
    @commands.is_owner()
    async def color_roles(self, ctx: commands.Context):
        """Color role embed"""
        embed = nextcord.Embed(
            title="__**Color Roles**__",
            description="Click on a button to select a color"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_author(
            name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        embed.set_footer(text="Bot is running v1.0.0")
        embed.add_field(name="__**Colors**__", value=f"*Orange*: 🟠\n"
                        f"*Yellow*: 🟡\n"
                        f"*Green*:  🟢\n"
                        f"*Blue*:   🔵\n"
                        f"*Purple*: 🟣\n"
                        f"*Brown*:  🟤\n"
                        f"*White*:  ⚪\n"
                        f"*Maroon*: 🔴", inline=True)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed, view=ColorRoleView())

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.is_owner()
    async def dropdown(self, ctx):
        await ctx.send("Invalid sub-command specified")

    @dropdown.command(name="lang")
    @commands.is_owner()
    async def lang(self, ctx):
        """lang test command"""
        view = DropdownView()
        await ctx.send('choose a language!', view=view)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def server(self, ctx):
        """server lockdown commands."""
        await ctx.channel.trigger_typing()
        await ctx.send("Invalid sub-command passed")

    @server.command(name="lock")
    @commands.has_permissions(administrator=True)
    async def _lock(self, ctx, *, channel: nextcord.TextChannel = None):
        "Lockdown the server."
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False, read_messages=None, view_channel=False)
        await ctx.channel.trigger_typing()
        await ctx.send('locked down server 🔒')

    @server.command(name="unlock")
    @commands.has_permissions(administrator=True)
    async def _unlock(self, ctx, *, channel: nextcord.TextChannel = None):
        """Unlockdown the server."""
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name} with --server", send_messages=None, read_messages=None, view_channel=False)
        await ctx.channel.trigger_typing()
        await ctx.send('unlocked server 🔒')

    @server.command(name="invite")
    async def invite(self, ctx):
        """A useful command that displays a permanent invite link."""
        embed = nextcord.Embed(
            title="__Permanent Invite Link__",
            description="https://discord.gg/dm7gSAT68d",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)

    @server.command(name="suggest")
    async def suggest(self, ctx, *, suggestion):
        await ctx.channel.purge(limit=1)  # purge
        channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
        suggest = nextcord.Embed(
            title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
        sugg = await channel.send(embed=suggest)
        await sugg.add_reaction('✅')
        await sugg.add_reaction('❌')
        suggest2 = nextcord.Embed(
            title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
        suggest2.add_field(name='Msg ID:', value=f'{sugg.id}', inline=False)
        await sugg.edit(embed=suggest2)

    @server.command(name="approve")
    async def approve(self, ctx, id: int = None, *, reason=None):
        await ctx.channel.purge(limit=1)
        if id is None:
            return
        channel = await ctx.guild.fetch_channel(config.SERVER_SUGGESTION_CHANNEL_ID)
        if channel is None:
            return
        suggestionMsg = await channel.fetch_message(id)
        embed = nextcord.Embed(title=f'Suggestion has been approved',
                               description=f'Suggestion `{suggestionMsg.id}` has been approved by {ctx.author.name} | reason: {reason}')
        Msg = await channel.send(embed=embed)
        await Msg.add_reaction('✅')

    @server.command(name="deny")
    async def deny(self, ctx, id: int = None, *, reason=None):
        await ctx.channel.purge(limit=1)
        if id is None:
            return
        channel = await ctx.guild.fetch_channel(config.SERVER_SUGGESTION_CHANNEL_ID)
        if channel is None:
            return
        suggestionMsg = await channel.fetch_message(id)
        embed = nextcord.Embed(title=f'Suggestion has been denied',
                               description=f'Suggestion `{suggestionMsg.id}` has been denied by {ctx.author.name}')
        embed.add_field(name='reason:', value=f'{reason}')
        Msg = await channel.send(embed=embed)
        await Msg.add_reaction('❌')

    @commands.group()
    @commands.guild_only()
    @commands.is_owner()
    async def rules(self, ctx):
        """Rules commands"""
        await ctx.send("Invalid sub-command passed.")

    @rules.command(name="sysbot")
    @commands.is_owner()
    async def sysbot(self, ctx):
        """A useful command that displays sysbot rules."""
        version = "v1.1.0"

        embed = nextcord.Embed(
            title="__**Greninja SysBot Rules**__",
            description="Anyone who break the rules or is just straight up a pain in the ass about it, gets access revoked, to either the bot or the server. \n\n1. Don't try anything illegal, it won't work. \n2. You've tried everything and it still isn't legal, DM or ping <@&858153204146634782> \n2. Help can be asked, we won't shy away from it just make sure you've read<#858130122221420554> first. \n3. Anyone who uses it, does so at their own discretion. Don't be that person to call others out for using it. \n4. First try? Checkout <#858130122221420554> \n5. Made anything with the bot and you go sell it, insta-ban, no excuses.\n6. Refrain from deleting messages, even if it's a spelling mistake.  \n8. Have fun and Be respectful\n9. Using the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n10. No code sharing. The bot is for this server only\n\nBot access will be revoked for multiple offenders.\n\nRequests for special mons can be made in <#865074053759893525> , The PK8 Master will get to it as soon as he can.\n\nTo get access to the bots click below!\n🤖: Greninja SysBot Access",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)

    @rules.command(name="guild")
    @commands.is_owner()
    async def guild(self, ctx):
        """A useful command that displays server rules."""
        version = "v1.1.0"

        embed = nextcord.Embed(
            title=f"__Greninja SysBot Commands__",
            description=f"\n<:Switch:865465921040678932> __**The Rules**__ <:Switch:865465921040678932>\n\n"
            f"1. Full compliance to Discord's ToS.\n"
            f"2. Absolutely no drama.\n"
            f"3. Got issues with someone, talk to <@&829942684947841024>  or <@&867254914563178527> or resolve it in DM's.\n"
            f"4. Keep your -isms IRL and not in here.\n"
            f"5. You've got 3 strikes, so don't be that person.\n"
            f"6. Invite your friends, yet keep the Drama Queens out.\n"
            f"7. Please keep Politics and Religion out, we don't mind a healthy discussion, but DMs are best suited for that.\n"
            f"8. We allow pinging each other, demanding not to get pinged will get you a warning.\n"
            f"9. We don't mind cussing, sarcasm or sexually tinted jokes, but keep porn out.\n"
            f"10. Don't ask or distribute illegal Pokémon, talk is permitted (Use `!illegal` for a list).\n"
            f"11. No selling of any kind. (unless approved by an admin).\n"
            f"12. Don't DM other members unless you have their permission to do so.\n\n"
            f"This can be updated for future reference.\n\n"
            f"Click :thumbsup:Confirm to gain access to the rest of the server!\n\n"
            f"Then visit <#861616591199141908> to give yourself some roles and <#868914000572846120> for Sys-Bot access!\n\n"
            f"https://discord.gg/dm7gSAT68d\n\n"
            f"Server and Bot rules subject to change.\n\n"
            f"<a:rainbowmeltandab:866027057691230229>\n\n",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Interactions(bot))
