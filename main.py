from time import sleep
from setup import setup
from conversation import Conversation
from tools.tools_list import get_all_tools
import apple_db.imessages as imessages

setup(update_vector_stores=False)

def loop():
    unread_messages = imessages.get_unread_messages(get_sender_info=True, group_chats=False, unique_senders_only=True)
    tools = get_all_tools(web_search=True, file_search=True)
    conversations = {}

    for message in unread_messages:
        conversations[message["sender_id"]] = Conversation(message, max_length=20, tools=tools)
        conversations[message["sender_id"]].respond()

    while True:
        print("Checking for new messages...")
        for conversation in conversations.values():
            new_messages = conversation.check_for_new_messages()
            if new_messages:
                conversation.respond()
        print("Sleeping for 5 seconds...")
        sleep(5)

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print("Shutting down...")
        exit(0)