import json

def get_user_info():
    with open("./knowledgebase/personal_network.json", "r") as f:
        contacts = json.load(f)
    for contact in contacts:
        if "self" in contact["relation"]:
            return contact
    return None

MAC_USER = "sohan"
USER = get_user_info()