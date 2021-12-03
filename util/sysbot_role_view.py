import config
import nextcord
from util.role_view import RoleView
from utils.utils import custom_id

VIEW_NAME = "SysBotRuleView"


class SysBotRuleView(RoleView):
    def __init__(self):
        super().__init__(required_roles=[config.MEMBER_ROLE_ID])

    @nextcord.ui.button(
        label="I Agree",
        emoji="<:Frogadier:899243354980761610>",
        style=nextcord.ButtonStyle.blurple,
        # set custom id to be the bot name : the class name : the role id
        custom_id=custom_id(VIEW_NAME, config.FROGADIER_ROLE_ID),
    )
    async def subscriber_button(self, button, interaction):
        await self.handle_click(button, interaction)




