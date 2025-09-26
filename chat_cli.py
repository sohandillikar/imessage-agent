import openai_utils
from setup import setup
import knowledge_base.people.utils as people_utils

client = setup(update_knowledge_base=False)

sender_id = "+15107503277"
person = people_utils.get_person_info_by_sender_id(sender_id)
first_name = person["full_name"].split(" ")[0]

tools = openai_utils.get_all_tools(web_search=True, file_search=True)
system_prompt = openai_utils.create_system_prompt(sender_id=sender_id)
messages = [{"role": "system", "content": [{"type": "input_text", "text": system_prompt}]}]

print(f"System prompt: {system_prompt}")

while True:
    user_input = input(f"{first_name}: ")
    messages.append({"role": "user", "content": [{"type": "input_text", "text": f"{first_name}: {user_input}"}]})
    response, messages = openai_utils.create_response(client, messages, tools=tools)
    if len(messages) > 20:
        messages = messages[-20:]
    print(f"{response.output_text} ({response.usage.total_tokens} tokens)\n")