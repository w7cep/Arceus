import nextcord
from nextcord import Embed
from nextcord.ext import commands
import config
from better_profanity import profanity
from datetime import datetime
import asyncio
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
    async def on_message(self, message):
        def _check(m):
            return (m.author == message.author
                    and len(m.mentions)
                    and (datetime.utcnow()-m.created_at).seconds < 60)

        if message.content == "!d bump":
            await message.channel.send("That was a good bumping!\nI will remind you in 2 hours for another!")
            await asyncio.sleep(7200)
            await message.channel.send("<@&881596772143759400> I'm ready for another good bumping!")
#7200 seconds = 2 hours

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
