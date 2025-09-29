import openai_utils
from setup import setup
import apple_db.imessages as imessages
from tools.tools_list import get_all_tools
import tools.people.utils as people_utils

client = setup(update_knowledge_base=False)

unread_messages = imessages.get_unread_messages(get_sender_info=True)