from nextcord.ext import commands, tasks
import nextcord
import datetime
import nextcord.errors
from nextcord.ext.commands import MissingPermissions

from utils.util import Pag
from nextcord.ext import commands
import nextcord.ext

class Infractions(commands.Cog, name="Infractions"):
    """Receives ping commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: nextcord.Member, *, reason):
        if member.id in [ctx.author.id, self.bot.user.id]:
            return await ctx.send("You cannot warn yourself or the bot!")

        current_warn_count = len(
            await self.bot.warns.find_many_by_custom(
                {
                    "user_id": member.id,
                    "guild_id": member.guild.id
                }
            )
        ) + 1
        
        warn_filter = {"user_id": member.id, "guild_id": member.guild.id, "number": current_warn_count}
        warn_data = {"reason": reason, "timestamp": ctx.message.created_at, "warned_by": ctx.author.id}
        
        await self.bot.warns.upsert_custom(warn_filter, warn_data)
        
        embed = nextcord.Embed(
            title="You are being warned:",
            description=f"__**Reason**__:\n{reason}",
            colour=nextcord.Colour.red(),
            timestamp=ctx.message.created_at
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_footer(text=f"Warn: {current_warn_count}")
        
        try:
            await member.send(embed=embed)
            await ctx.send("Warned that user in dm's for you.")
        except nextcord.HTTPException:
            await ctx.send(member.mention, embed=embed)
            
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def warns(self, ctx, member: nextcord.Member):
        warn_filter = {"user_id": member.id, "guild_id": member.guild.id}
        warns = await self.bot.warns.find_many_by_custom(warn_filter)
        
        if not bool(warns):
            return await ctx.send(f"Couldn't find any warns for: `{member.display_name}`")
        
        warns = sorted(warns, key=lambda x: x["number"])
        
        pages = []
        for warn in warns:
            description = f"""
            Warn Number: `{warn['number']}`
            Warn Reason: `{warn['reason']}`
            Warned By: <@{warn['warned_by']}>
            Warn Date: {warn['timestamp'].strftime("%I:%M %p %B %d, %Y")}
            """
            pages.append(description)
        
        await Pag(
            title=f"Warns for `{member.display_name}`",
            colour=0xCE2029,
            entries=pages,
            length=1
        ).start(ctx)

    @commands.command(aliases=["delwarn", "dw"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def deletewarn(self, ctx, member: nextcord.Member, warn: int = None):
        """Delete a warn / all warns from a given member"""
        filter_dict = {"user_id": member.id, "guild_id": member.guild.id}
        if warn:
            filter_dict["number"] = warn

        was_deleted = await self.bot.warns.delete_by_custom(filter_dict)
        if was_deleted and was_deleted.acknowledged:
            if warn:
                return await ctx.send(
                    f"I deleted warn number `{warn}` for `{member.display_name}`"
                )

            return await ctx.send(
                f"I deleted `{was_deleted.deleted_count}` warns for `{member.display_name}`"
            )

        await ctx.send(
            f"I could not find any warns for `{member.display_name}` to delete matching your input"
        )

def setup(bot: commands.Bot):
    bot.add_cog(Infractions(bot))