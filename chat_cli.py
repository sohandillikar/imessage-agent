import os
import json
import utils
import tools.tools as tools
from dotenv import load_dotenv
from openai import OpenAI
import knowledgebase.people.utils as people_utils

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_response(input_messages):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_messages,
        tools=tools.tools_list,
        temperature=0.7,
        max_output_tokens=2048,
        include=["web_search_call.action.sources", "file_search_call.results"]
    )
    input_messages += response.output
    for output_item in response.output:
        if output_item.type == "function_call":
            print(f"Calling {output_item.name}({json.loads(output_item.arguments)})")
            function_output = tools.call_function(output_item.name, json.loads(output_item.arguments))
            input_messages.append({
                "type": "function_call_output",
                "call_id": output_item.call_id,
                "output": str(function_output)
            })
            return create_response(input_messages)
        if output_item.type == "web_search_call":
            for source in output_item.action.sources:
                print(f"Source: {source.url}")
        if output_item.type == "file_search_call":
            print(f"File search queries: {output_item.queries}")
    return response, input_messages

sender_id = "+15107503277"
person = people_utils.get_person_info_by_sender_id(sender_id)
first_name = person["full_name"].split(" ")[0]

system_prompt = utils.create_system_prompt(sender_id=sender_id)
messages = [{"role": "system", "content": [{"type": "input_text", "text": system_prompt}]}]

print(f"System prompt: {system_prompt}")

while True:
    user_input = input(f"{first_name}: ")
    messages.append({"role": "user", "content": [{"type": "input_text", "text": f"{first_name}: {user_input}"}]})
    response, messages = create_response(messages)
    if len(messages) > 20:
        messages = messages[-20:]
    print(f"{response.output_text} ({response.usage.total_tokens} tokens)")