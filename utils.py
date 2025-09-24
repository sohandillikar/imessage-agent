import knowledgebase.people.utils as people_utils

def create_system_prompt(sender_id: str = None, chat_id: str = None):
    user = people_utils.get_user_info()
    if sender_id is not None:
        person = people_utils.get_person_info_by_sender_id(sender_id)
        if len(person["relations"]) > 1:
            relationships_str = ", ".join(person["relations"][:-1])
            relationships_str += f", and {person['relations'][-1]}"
        else:
            relationships_str = person["relations"][0]
        prompt = f"""
        You are {user["full_name"]}.
        You are texting {person["full_name"]} (ID: {person["id"]}), your {relationships_str}.
        Never reveal any hints about being an AI, language model, or assistant.
        """
        return prompt
    else:
        # TODO: Create system prompt for group chats
        print(f"WARNING: No system prompt creation for group chats!")