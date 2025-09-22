import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_response(input_messages):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=input_messages,
        tools=tools,
        temperature=0.7,
        max_output_tokens=2048,
        include=["web_search_call.action.sources"]
    )
    input_messages += response.output
    for output_item in response.output:
        if hasattr(output_item, "action"):
            for source in output_item.action.sources:
                print(f"Source: {source.url}")
        if output_item.type == "function_call":
            print(f"Calling {output_item.name}({json.loads(output_item.arguments)})")
            function_output = call_function(output_item.name, json.loads(output_item.arguments))
            input_messages.append({
                "type": "function_call_output",
                "call_id": output_item.call_id,
                "output": str(function_output)
            })
            return create_response(input_messages)
    return response, input_messages

# system_prompt = "You are a helpful assistant that can answer questions and help with tasks."
# messages = [{"role": "system", "content": [{"type": "input_text", "text": system_prompt}]}]
messages = []

while True:
    user_input = input("You: ")
    messages.append({"role": "user", "content": [{"type": "input_text", "text": user_input}]})
    response, messages = create_response(messages)
    if len(messages) > 20:
        messages = messages[-20:]
    print(f"{response.output_text} ({response.usage.total_tokens} tokens)")