import ast
import json
from config import *

def sql_output_to_json(output: list[tuple], columns: list[tuple]) -> list[dict]:
    for i, row in enumerate(output):
        output[i] = {columns[j][0] : row[j] for j in range(len(columns))}
    return output

def python_to_json_type(python_type: str) -> str:
    if python_type == "str":
        return "string"
    elif python_type in ["int", "float"]:
        return "number"
    elif python_type == "bool":
        return "boolean"
    elif python_type in ["list", "tuple"]:
        return "array"
    elif python_type == "dict":
        return "object"
    else:
        print(f"WARNING: Unknown type '{python_type}'!")
        return "string"

def get_arg_description(arg_name: str, docstring: str) -> str:
    for line in docstring.split("\n"):
        line = line.strip()
        if line.startswith(f"{arg_name}:"):
            description = line.replace(f"{arg_name}:", "", 1).strip()
            return description
    return None

# TODO: Modify for enum (https://platform.openai.com/docs/guides/function-calling)
# TODO: Create config file for web search location
def get_tools_list(file_path: str, avoid_functions: list[str] = [], web_search: bool = False) -> list[dict]:
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    
    tools = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name not in avoid_functions:
            function_name = node.name
            description = ast.get_docstring(node)
            properties = {}
            required = []
            required_args = len(node.args.args) - len(node.args.defaults)

            for i, arg in enumerate(node.args.args):
                arg_name = arg.arg
                arg_type = python_to_json_type(ast.unparse(arg.annotation))
                arg_description = get_arg_description(arg.arg, description)
                if arg_description is None:
                    print(f"WARNING: No description found for '{arg_name}' in {function_name}!")
                    arg_description = ""
                properties[arg_name] = {"type": arg_type, "description": arg_description}
                if i < required_args:
                    required.append(arg_name)
            
            tools.append({
                "type": "function",
                "name": function_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            })
    
    if web_search:
        tools.append({
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "US",
                "timezone": "America/Los_Angeles"
            }
        })
    
    return tools

def get_personal_network() -> list[dict]:
    with open("./knowledgebase/personal_network.json", "r") as f:
        return json.load(f)

def get_personal_contact(sender_id: str) -> dict:
    personal_network = get_personal_network()
    for contact in personal_network:
        if contact["phone"] == sender_id or contact["email"] == sender_id:
            return contact
    return None

def create_system_prompt(sender_id: str, chat_id: str = None):
    if chat_id is None:
        personal_contact = get_personal_contact(sender_id)
        if len(personal_contact["relation"]) == 1:
            personal_contact_relationships = personal_contact["relation"][0]
        else:
            personal_contact_relationships = ", ".join(personal_contact["relation"][:-1])
            personal_contact_relationships += f", and {personal_contact['relation'][-1]}"
        prompt = f"""
        You are {USER["full_name"]}.
        You are texting {personal_contact["full_name"]}, your {personal_contact_relationships}.
        Never reveal any hints about being an AI, language model, or assistant.
        """
        return prompt
    else:
        # TODO: Create system prompt for group chats
        print(f"WARNING: No system prompt creation for group chats!")