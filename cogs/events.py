import nextcord
from nextcord import Embed
from nextcord.ext import commands
import config
from better_profanity import profanity
from datetime import datetime

profanity.load_censor_words_from_file("./data/profanity.txt")

class Events(commands.Cog, name="Events"):
    """Test commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        '''self.bot_reminder.start()'''

    '''@tasks.loop(hours=4)  # you can even use hours and minutes
    async def bot_reminder(self):
        print("Sending SysBot reminder message")
        channel = self.bot.get_channel(843271842931933224)
        await channel.send("**Reminder**\n\nUsing the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n\nPlease don't delete messages. Even when it's a mistake.\nMakes trouble-shooting difficult.\n\nBot access will be revoked for multiple offenders.")

    @bot_reminder.before_loop
    async def before_bot_reminder(self):
        print('waiting...')
        await self.bot.wait_until_ready()'''

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        """Welcome members when they join"""
        guild = self.bot.get_guild(config.GUILD_ID)
        intro_channel = guild.get_channel(config.INTRO_CHANNEL_ID)
        rules_channel = guild.get_channel(config.RULES_CHANNEL_ID)
        bot_rules_channel = guild.get_channel(config.BOT_RULES_CHANNEL_ID)
        # don't welcome bots or members of other guilds the bot is in
        if member.bot or guild != member.guild:
            return
        # send welcome message
        await intro_channel.send(
            f"Welcome to **Greninja's Grotto**, {member.mention}!\n"
            f"Please read the rules in {rules_channel.mention} to gain access to the rest of the server!\n\nThen head over to {bot_rules_channel.mention} to gain access to the SysBot!"
        )
        # give inital "access" role
        await member.add_roles(guild.get_role(config.ACCESS_ROLE_ID))
        # give the "unassigned" role
        await member.add_roles(guild.get_role(config.UNASSIGNED_ROLE_ID))

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        """Say goodbye to members."""
        guild = self.bot.get_guild(config.GUILD_ID)
        outro_channel = guild.get_channel(config.OUTRO_CHANNEL_ID)
        if member.bot or guild != member.guild:
            return
        await outro_channel.send(f"Peace! :middle_finger: {member.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        def _check(m):
            return (m.author == message.author
                    and len(m.mentions)
                    and (datetime.utcnow()-m.created_at).seconds < 60)

        if profanity.contains_profanity(message.content):
            await message.delete()
            await message.channel.send("You can't use that word here.", delete_after=10)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        log_channel = self.bot.get_channel(913732668263399456)
        if before.name != after.name:
            embed = Embed(title="Username change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(title="Discriminator change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

        if before.avatar.url != after.avatar.url:
            embed = Embed(title=f"Avatar change for {before.name}{before.discriminator}",
                          description=f"New image is below, old to the right.",
                          timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar.url)
            embed.set_image(url=after.avatar.url)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = self.bot.get_channel(913732668263399456)
        if before.display_name != after.display_name:
            embed = Embed(title="Nickname change for",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title="Role updates",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                      ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(913732668263399456)
        if not after.author.bot:
            if before.content != after.content:
                embed = Embed(title="Message edit",
                              description=f"Edit by {after.author.display_name}.",
                              colour=after.author.colour,
                              timestamp=datetime.utcnow())

                fields = [("Before", before.content, False),
                          ("After", after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(913732668263399456)
        if not message.author.bot:
            embed = Embed(title="Message deletion",
                          description=f"Action by {message.author.display_name}.",
                          colour=message.author.colour,
                          timestamp=datetime.utcnow())

            fields = [("Content", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await log_channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
