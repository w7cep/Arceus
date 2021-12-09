import nextcord
from nextcord.ext import commands
import asyncio
import datetime
from datetime import datetime
from typing import List
from utils.utils import custom_id
import config

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------


class ApplyView(nextcord.ui.View):
    def __init__(self, add_only: bool = False, required_roles: List[int] = None):
        """
        Args:
            add_only - if True, only add the role, if False, remove it too
        """
        super().__init__(timeout=None)
        self.__add_only = add_only
        self.__required_roles = required_roles or []

    def _check_required_roles(self, user: nextcord.Member):
        user_roles_ids = [role.id for role in user.roles]
        return all(role_id in user_roles_ids for role_id in self.__required_roles)

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        # get role from the button's role id
        role = interaction.guild.get_role(int(button.custom_id.split(":")[-1]))
        assert isinstance(role, nextcord.Role)
        # if member has the role, remove it
        if role in interaction.user.roles:
            # don't remove if add_only flag is set
            if self.__add_only:
                return await interaction.response.send_message(
                    f"You already have the {role.name} role!", ephemeral=True
                )
            # remove the role
            await interaction.user.remove_roles(role)
            # send confirmation message
            return await interaction.response.send_message(
                f"Your {role.name} role has been removed", ephemeral=True
            )
        # check for required roles
        if not self._check_required_roles(interaction.user):
            return await interaction.response.send_message(
                f"Please confirm above that you have read the rules.", ephemeral=True
            )
        # if the member does not have the role, add it
        await interaction.user.add_roles(role)
        # remove unassigned role
        unassigned_role = interaction.guild.get_role(config.UNASSIGNED_ROLE_ID)
        if unassigned_role in interaction.user.roles:
            await interaction.user.remove_roles(unassigned_role)
        # send confirmation message
        await interaction.response.send_message(
            f"You have been given the {role.name} role", ephemeral=True
        )

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------

class ApplyConfirm(ApplyView):
    def __init__(self):
        super().__init__(add_only=True, required_roles=[config.MEMBER_ROLE_ID],)
    VIEW_NAME = "ApplyConfirm"
    @nextcord.ui.button(
        label="Approve",
        emoji="✅",
        style=nextcord.ButtonStyle.blurple,
        # set custom id to be the bot name : the class name : the role id
        custom_id=custom_id(VIEW_NAME, config.MODERATOR_ROLE_ID),
    )
    async def application_button(self, button, interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label="Deny", emoji="❌", style=nextcord.ButtonStyle.grey , custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()


#----------------------------------------------------------------------------------------------------------------------------------------------------------

class App(commands.Cog, name="App"):
    """Application to become a moderator"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

#----------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.guild_only()
    async def apply(self, ctx):
        view = ApplyConfirm()

        # we will make a list of questions here and you may add as more as you like
        questions = ["Do you have two-factor authentication (2FA) set up on your discord account?", "What continent are you on?", "Please enter today's date in your time zone.", "Please enter the current time in your time zone, doesn't have to be super accurate.", "Please enter your general availability. eg: weekdays 5pm-9pm, some weekends all day. This does not have to be precise and will not be enforced.", "Do you have a modded/CFW/hacked and unbanned switch?", "Have/Do you use the pokemon bots on Greninj's Grotto?", "How familiar with pkhex are you? None,Somewhat,Very", "Is your profile picture on discord fairly safe?", "Are you generally not unreasonably argumentative?", "Do you enjoy helping others when you have time?", "Have you read and understand most of the bot instructions on the server?", "Do you believe you are active on the server?", "Do you have experience as a mod in other Discord servers?", "Please explain why you would want to join the moderation team in as many or as few words as you would like."]

        answers = [] # this will be an empty list of answers because it will be filled with the user's responses

        for question in questions:  # this is a for loop that will do the same code below for every question in our questions list
            # this will get the order of the question in the questions list
            question_order = questions.index(question)
            # since the index starts with the number 0, this will add 1 to the index number
            question_number = question_order + 1
            question_msg = await ctx.author.send(f"**Q{question_number} : {question}**\nA : Type your answer...")

            def check(msg):  # this is a check that we will use in the `wait_for` to make sure the user responding is the command author and the response is in the bot's DMs
                return msg.author == ctx.author and msg.guild == None

            # this will wait for a response from the command author
            answer = await self.bot.wait_for('message', check=check)
            # this will edit the message of the question to make sure the response is recorded
            await question_msg.edit(f"**Q : {question}**\nA : {answer.content}")
            # this will append the answer in the answers list with the answer's number
            answers.append(f"A{question_number} : {answer.content}")

        # get the channel that the applications should be sent to
        apps_logs_channel = self.bot.get_channel(918060994855575582)

        embed = nextcord.Embed(
                color=nextcord.Color.purple(),
            )  # creating Embed instance

        embed.set_author(
            name=f"Staff application by {ctx.author}", icon_url=ctx.author.avatar.url)

        for question in questions:  # this is a for loop that will add a field to the embed for every question
            question_order = questions.index(question)
            question_number = question_order + 1

            # now we will need to detect the question's answer

            for answer in answers:  # this will check for the answer in all the answers
                # as we saved the answer "A{question_number} : {answer.content}"
                if answer.startswith(f"A{question_number}"):
                    a = answer

            # this will add a field to the embed
            embed.add_field(name=question, value=a, inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/862327803964817438/907116113970741328/21035.jpg")
        await apps_logs_channel.send(embed=embed, view=view)
        await ctx.author.send("Your application has been submitted!")

        await view.wait()

        if view.value is None:
            await ctx.author.send("Command has been Timed Out, please try again.")

        elif view.value:
            await apps_logs_channel.send(f"You approved {ctx.author.mention} to be a moderator!")

        else:
            await apps_logs_channel.send(f"You denied **{ctx.author.name}#{ctx.author.discriminator}'s** application to be a moderator!")
        return

#----------------------------------------------------------------------------------------------------------------------------------------------------------

def setup(bot: commands.Bot):
    bot.add_cog(App(bot))