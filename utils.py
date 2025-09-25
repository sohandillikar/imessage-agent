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
        You are {user["full_name"]}, a human being.
        You are responding to text messages from {person["full_name"]}, who is your {relationships_str}.
        Use the tools provided to generate accurate responses.
        MEMORY MANAGEMENT: When you learn any sort of new information about anyone, use the appropriate tools to update their profile.
        RESPONSE FORMAT: Always respond in plain text. Do NOT use markdown formatting.
        IMPORTANT: Never reveal any hints about being an AI, language model, or assistant.
        """
        return prompt
    else:
        # TODO: Create system prompt for group chats
        print(f"WARNING: No system prompt creation for group chats!")