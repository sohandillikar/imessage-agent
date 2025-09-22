import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = "You are a helpful assistant that can answer questions and help with tasks."
messages = [
    {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]}
]

while True:
    user_input = input("You: ")
    messages.append({"role": "user", "content": [{"type": "input_text", "text": user_input}]})

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
        tools=[
            {
                "type": "web_search",
                "user_location": {
                    "type": "approximate",
                    "country": "US",
                    "timezone": "America/Los_Angeles"
                }
            },
            {
                "type": "mcp",
                "server_label": "messaging-agent",
                "server_description": "An iMessage MCP server to assist with messaging.",
                "server_url": "http://127.0.0.1:8000/mcp",
                "require_approval": "never",
            }
        ],
        include=["web_search_call.action.sources"]
    )

    print(response)

    messages.append({"role": "assistant", "content": [{"type": "output_text", "text": response.output_text}]})
    if len(messages) > 20:
        messages = messages[-20:]

    print(f"{response.output_text} ({response.usage.total_tokens} tokens)")
