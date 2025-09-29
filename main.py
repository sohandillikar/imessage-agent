import apple_db.imessages as imessages
from tools.tools_list import get_all_tools
from conversation import Conversation
from time import sleep

def loop():
    unread_messages = imessages.get_unread_messages(get_sender_info=True, group_chats=False, unique_senders_only=True)
    tools = get_all_tools(web_search=True, file_search=True)
    conversations = {}

    for message in unread_messages:
        conversations[message["sender_id"]] = Conversation(message, max_length=20, tools=tools)
        conversations[message["sender_id"]].respond()

    while True:
        for conversation in conversations.values():
            new_messages = conversation.check_for_new_messages()
            if new_messages:
                conversation.respond()
        sleep(5)

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print("Saving conversations...")
        exit(0)