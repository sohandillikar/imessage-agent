import os
import sys
import json
import apple_db.imessages as imessages
import tools.people.utils as people_utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import openai_utils

def get_permissions() -> dict:
    with open("config.json", "r") as f:
        config = json.load(f)
    return config["conversation_permissions"]

def update_messages(messages: list[dict]) -> None:
    with open("knowledge_base/messages.json", "w") as f:
        json.dump(messages, f, indent=4)
    vector_store = openai_utils.get_vector_store("knowledge_base")
    openai_utils.update_vector_store(vector_store, ["knowledge_base/messages.json"])

def load_messages() -> list[dict]:
    permissions = get_permissions()
    all_messages = []
    user = people_utils.get_user()
    for sender_id in permissions.keys():
        if permissions[sender_id]["read"]:
            person = people_utils.get_person_by_sender_id(sender_id)
            messages = imessages.get_messages(options=f"sender_id='{sender_id}'")
            for message in messages:
                if message["content"]:
                    all_messages.append({
                        "timestamp": message["dt"],
                        "from": user["full_name"] if message["is_from_me"] == 1 else person["full_name"],
                        "to": person["full_name"] if message["is_from_me"] == 1 else user["full_name"],
                        "content": message["content"]
                    })
    update_messages(all_messages)
    return all_messages