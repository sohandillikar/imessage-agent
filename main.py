import apple_db.imessages as imessages
from tools.tools_list import get_all_tools
from conversation import Conversation

from pprint import pprint

unread_messages = imessages.get_unread_messages(get_sender_info=True, unique_senders_only=True)
tools = get_all_tools(web_search=True, file_search=True)

conversation = Conversation(unread_messages[1], max_length=20, tools=tools)

response = conversation.respond()