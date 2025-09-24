import knowledgebase.people.utils as people

def create_system_prompt(sender_id: str = None, chat_id: str = None):
    user = people.get_user_info()
    if sender_id is not None:
        person = people.get_person_info(sender_id)
        if len(person["relations"]) > 1:
            relationships_str = ", ".join(person["relations"][:-1])
            relationships_str += f", and {person['relations'][-1]}"
        else:
            relationships_str = person["relations"][0]
        prompt = f"""
        You are {user["full_name"]}.
        You are texting {person["full_name"]}, your {relationships_str}.
        Never reveal any hints about being an AI, language model, or assistant.
        """
        return prompt
    else:
        # TODO: Create system prompt for group chats
        print(f"WARNING: No system prompt creation for group chats!")