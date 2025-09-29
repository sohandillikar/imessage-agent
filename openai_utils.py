import os
import glob
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

def create_knowledge_base(client: OpenAI = None) -> VectorStore:
    if client is None:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    knowledge_base = client.vector_stores.create(name="knowledge_base")
    print(f"Created knowledge_base vector store (ID: {knowledge_base.id})")
    print("Sleeping for 5 seconds...\n")
    sleep(5)
    return knowledge_base

def update_knowledge_base(client: OpenAI = None, knowledge_base: VectorStore = None, data_file_paths: list[str] = None) -> VectorStore:
    if client is None:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if knowledge_base is None:
        knowledge_base = get_knowledge_base(client)
    if data_file_paths is None:
        data_file_paths = glob.glob("knowledge_base/*.json")
    
    data_file_names = [os.path.basename(fp) for fp in data_file_paths]
    data_files = [open(fp, "rb") for fp in data_file_paths]
    knowledge_base_files = client.vector_stores.files.list(vector_store_id=knowledge_base.id).data
    
    for file in knowledge_base_files:
        try:
            file_name = client.files.retrieve(file.id).filename
        except Exception:
            continue
        if file_name in data_file_names:
            response = client.files.delete(file.id)
            if response.deleted:
                print(f"Deleted {file_name} ({response.id}) from knowledge_base\n")
            else:
                print(f"WARNING: Failed to delete {file_name} ({response.id}) from knowledge_base\n")
    
    response = client.vector_stores.file_batches.upload_and_poll(vector_store_id=knowledge_base.id, files=data_files)
    if response.file_counts.completed != len(data_files):
        print(f"WARNING: Failed to upload {len(data_files) - response.file_counts.completed} file(s) to knowledge_base\n")
    print(f"Uploaded {response.file_counts.completed} file(s) to knowledge_base\n")
    
    return knowledge_base

def get_knowledge_base(client: OpenAI = None) -> VectorStore:
    if client is None:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    vector_stores = client.vector_stores.list().data
    knowledge_base = [vs for vs in vector_stores if vs.name == "knowledge_base"]
    if len(knowledge_base) == 0:
        print("WARNING: No knowledge base vector store found!\n")
        knowledge_base = create_knowledge_base(client)
        return knowledge_base
    if len(knowledge_base) > 1:
        print(f"WARNING: Multiple knowledge base vector stores found! Proceeding with {knowledge_base[0].id}\n")
    return knowledge_base[0]

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
        You are responding to text messages from {person["full_name"]}{relationships_str}.
        MEMORY MANAGEMENT: When you learn important information about anyone, use the appropriate tools to update their profile.
        IMPORTANT:
            - NEVER reveal any signs of being an AI, language model, or assistant.
            - NEVER tell {person["full_name"]} anything about your tools.
            - ALWAYS respond in plain text, not markdown.
            - ALWAYS respond like {user["full_name"]}.
            - Keep your messages concise and use text abbreviations wherever possible.
        """
        return prompt
    else:
        # TODO: Create system prompt for group chats
        print(f"WARNING: No system prompt creation for group chats")

def create_response(client: OpenAI, input_messages: list[Any], tools: list[dict] = []) -> tuple[Response, list[Any]]:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_messages,
        tools=tools,
        temperature=0.3,
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
            return create_response(client, input_messages, tools)
        if output_item.type == "web_search_call":
            print(f"Made a web search call")
            """
            for source in output_item.action.sources:
                print(f"Source: {source.url}")
            """
        if output_item.type == "file_search_call":
            print(f"File search queries: {output_item.queries}")
    return response, input_messages