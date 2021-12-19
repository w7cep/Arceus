import os
from dotenv.main import load_dotenv

load_dotenv()

# Bot setup
PREFIX = os.getenv("PREFIX", "")
BOT_NAME = os.getenv("BOT_NAME", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ACCESS_ROLE_ID = int(os.getenv("ACCESS_ROLE_ID", ""))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID", ""))
UNASSIGNED_ROLE_ID = int(os.getenv("UNASSIGNED_ROLE_ID", ""))
MUTED_ROLE_ID = int(os.getenv("MUTED_ROLE_ID", ""))

# Discord Guild ID
GUILD_ID = int(os.getenv("GUILD_ID", ""))

# Discord Channel IDs
INTRO_CHANNEL_ID = int(os.getenv("INTRO_CHANNEL_ID", ""))
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID", ""))
BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID", ""))
BOT_RULES_CHANNEL_ID = int(os.getenv("BOT_RULES_CHANNEL_ID", ""))
OUTRO_CHANNEL_ID = int(os.getenv("OUTRO_CHANNEL_ID", ""))
BOT_START_CHANNEL_ID = int(os.getenv("BOT_START_CHANNEL_ID", ""))


# Discord Role IDs
FROGADIER_ROLE_ID = int(os.getenv("FROGADIER_ROLE_ID", ""))
TRADECORD_ROLE_ID = int(os.getenv("TRADECORD_ROLE_ID", ""))
GIVEAWAY_PING_ROLE_ID = int(os.getenv("GIVEAWAY_PING_ROLE_ID", ""))
SWORD_ROLE_ID = int(os.getenv("SWORD_ROLE_ID", ""))
SHIELD_ROLE_ID = int(os.getenv("SHIELD_ROLE_ID", ""))
MALE_ROLE_ID = int(os.getenv("MALE_ROLE_ID", ""))
FEMALE_ROLE_ID = int(os.getenv("FEMALE_ROLE_ID", ""))
OTHER_ROLE_ID = int(os.getenv("OTHER_ROLE_ID", ""))
ORANGE_ROLE_ID = int(os.getenv("ORANGE_ROLE_ID", ""))
YELLOW_ROLE_ID = int(os.getenv("YELLOW_ROLE_ID", ""))
GREEN_ROLE_ID = int(os.getenv("GREEN_ROLE_ID", ""))
BLUE_ROLE_ID = int(os.getenv("BLUE_ROLE_ID", ""))
PURPLE_ROLE_ID = int(os.getenv("PURPLE_ROLE_ID", ""))
BROWN_ROLE_ID = int(os.getenv("BROWN_ROLE_ID", ""))
WHITE_ROLE_ID = int(os.getenv("WHITE_ROLE_ID", ""))
MAROON_ROLE_ID = int(os.getenv("MAROON_ROLE_ID", ""))


BOT_BAN_ROLE_ID = int(os.getenv("BOT_BAN_ROLE_ID", ""))

#DEN_SUGGESTION_CHANNEL_ID = int(os.getenv("DEN_SUGGESTION_CHANNEL_ID", ""))
SERVER_SUGGESTION_CHANNEL_ID = int(os.getenv("SERVER_SUGGESTION_CHANNEL_ID", ""))
#LAIR_SUGGESTION_ = int(os.getenv("LAIR_SUGGESTION_", ""))

'''YOUTUBE_PING_ROLE_ID = int(os.getenv("YOUTUBE_PING_ROLE_ID", ""))
CONTENT_CREATOR_ROLE_ID = int(os.getenv("CONTENT_CREATOR_ROLE_ID", ""))
DEVELOPER_ROLE_ID = int(os.getenv("DEVELOPER_ROLE_ID", ""))
SUBSCRIBER_ROLE_ID = int(os.getenv("SUBSCRIBER_ROLE_ID", ""))'''

# Discord Message IDs
RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID", ""))
BOT_RULES_MESSAGE_ID = int(os.getenv("BOT_RULES_MESSAGE_ID", ""))

MODERATOR_ROLE_ID = int(os.getenv("MODERATOR_ROLE_ID", ""))
