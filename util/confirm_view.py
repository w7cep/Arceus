import config
import nextcord
from utils.utils import custom_id

from util.role_view import RoleView

VIEW_NAME = "ConfirmView"


class ConfirmView(RoleView):
    def __init__(self):
        super().__init__(add_only=True)

    @nextcord.ui.button(
        label="I Agree",
        emoji="<:Froakie:899243283337855046>",
        style=nextcord.ButtonStyle.green,
        custom_id=custom_id(VIEW_NAME, config.MEMBER_ROLE_ID),
    )
    async def confirm_button(self, button, interaction):
        await self.handle_click(button, interaction)
