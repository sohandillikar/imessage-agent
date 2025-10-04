import os
import json
from typing import Any
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
from tools.tools import call_function
from openai.types.vector_store import VectorStore
from openai.types.responses.response import Response
import tools.people.utils as people_utils

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# TODO: Add "purpose"
def create_vector_store(name: str) -> VectorStore:
    vector_store = client.vector_stores.create(name=name)
    print(f"Created {name} vector store (ID: {vector_store.id})")
    print("Sleeping for 5 seconds...\n")
    sleep(5)
    return vector_store

def get_vector_store(name: str) -> VectorStore:
    vector_stores = client.vector_stores.list().data
    vector_store = [vs for vs in vector_stores if vs.name == name]
    if len(vector_store) == 0:
        print(f"WARNING: No {name} vector store found!\n")
        vector_store = create_vector_store(name)
        return vector_store
    if len(vector_store) > 1:
        print(f"WARNING: Multiple vector stores found! Proceeding with {vector_store[0].name} (ID: {vector_store[0].id})\n")
    return vector_store[0]

def update_vector_store(vector_store: VectorStore, data_file_paths: list[str]) -> VectorStore:
    data_file_names = [os.path.basename(fp) for fp in data_file_paths]
    data_files = [open(fp, "rb") for fp in data_file_paths]
    vector_store_files = client.vector_stores.files.list(vector_store_id=vector_store.id).data
    for file in vector_store_files:
        try:
            file_name = client.files.retrieve(file.id).filename
        except Exception:
            continue
        if file_name in data_file_names:
            response = client.files.delete(file.id)
            if response.deleted:
                print(f"Deleted {file_name} ({response.id}) from {vector_store.name} vector store\n")
            else:
                print(f"WARNING: Failed to delete {file_name} ({response.id}) from {vector_store.name} vector store\n")
    response = client.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=data_files)
    if response.file_counts.completed != len(data_files):
        print(f"WARNING: Failed to upload {len(data_files) - response.file_counts.completed} file(s) to {vector_store.name} vector store\n")
    print(f"Uploaded {data_file_names} to {vector_store.name} vector store\n")
    return vector_store

def create_system_prompt(sender_id: str = None, chat_id: str = None) -> str:
    user = people_utils.get_user()
    if sender_id is not None:
        person = people_utils.get_person_by_sender_id(sender_id)
        relationships_str = ""
        if len(person["relations"]) > 1:
            relationships_str = ", ".join(person["relations"][:-1])
            relationships_str += f", and {person['relations'][-1]}"
        elif len(person["relations"]) == 1:
            relationships_str = person["relations"][0]
        if relationships_str:
            relationships_str = f", who is your {relationships_str}"
        prompt = f"""
        You are {user["full_name"]}, a human being.
        You are texting {person["full_name"]}{relationships_str}.
        Use the appropriate "journals" tools to retrieve relevant personal context about yourself, in order to provide accurate responses.
        MEMORY MANAGEMENT: When you learn something about anyone, use the "people" tools to update their profile.
        SCHEDULE MANAGEMENT: When any task, plan, event, activity, or reminder is being discussed, use the "gcal" tools to create, modify, or delete it.
        IMPORTANT:
            - NEVER reveal any signs of being an AI, language model, or assistant.
            - NEVER mention anything about your tools in your responses.
            - Ensure that you are responding to everything in the conversation. Do not neglect previous messages.
            - ALWAYS respond in {user["full_name"]}'s texting style.
        """
        return prompt
    else:
        # TODO: Create system prompt for group chats
        print(f"WARNING: No system prompt creation for group chats")

def create_response(input_messages: list[Any], tools: list[dict] = []) -> tuple[Response, list[Any]]:
    response = client.responses.create(
        model="gpt-4o-mini", # ft:gpt-4.1-2025-04-14:personal:imsg-exp-1:CFxzn7tj
        input=input_messages,
        tools=tools,
        temperature=0.7,
        max_output_tokens=2048,
        include=["file_search_call.results"] # "web_search_call.action.sources"
    )
    input_messages += response.output
    for output_item in response.output:
        if output_item.type == "function_call":
            print(f"Calling {output_item.name}({json.loads(output_item.arguments)})")
            function_output = call_function(output_item.name, json.loads(output_item.arguments))
            input_messages.append({
                "type": "function_call_output",
                "call_id": output_item.call_id,
                "output": str(function_output)
            })
            return create_response(input_messages, tools)
        if output_item.type == "web_search_call":
            print(f"Made a web search call")
            """
            for source in output_item.action.sources:
                print(f"Source: {source.url}")
            """
        if output_item.type == "file_search_call":
            print(f"File search queries: {output_item.queries}")
    return response, input_messages