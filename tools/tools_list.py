import os
import sys
import ast
import glob

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import openai_utils

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
        print(f"WARNING: Unknown type '{python_type}'")
        return "string"

def get_arg_description(arg_name: str, docstring: str) -> str:
    for line in docstring.split("\n"):
        line = line.strip()
        if line.startswith(f"{arg_name}:"):
            description = line.replace(f"{arg_name}:", "", 1).strip()
            return description
    return None

# TODO: Modify for enum (https://platform.openai.com/docs/guides/function-calling)
def get_tools_from_file(file_path: str, module_name: str = None, avoid_functions: list[str] = []) -> list[dict]:
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    tools = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name not in avoid_functions:
            function_name = node.name
            if module_name is not None:
                function_name = f"{module_name}-{function_name}"
            description = ast.get_docstring(node)
            properties = {}
            required = []
            required_args = len(node.args.args) - len(node.args.defaults)

            for i, arg in enumerate(node.args.args):
                arg_name = arg.arg
                arg_type = python_to_json_type(ast.unparse(arg.annotation))
                arg_description = get_arg_description(arg.arg, description)
                if arg_description is None:
                    print(f"WARNING: No description found for '{arg_name}' in {function_name}")
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
    
    return tools

def get_all_tools(web_search: bool = False, file_search: bool = False) -> list[dict]:
    tools = []
    tool_files = glob.glob("tools/**/tools.py", recursive=True)

    for file_path in tool_files:
        folder_name = file_path.split("/")[-2]
        tools += get_tools_from_file(file_path, module_name=folder_name, avoid_functions=["call_function"])
    
    if web_search:
        country = os.getenv("COUNTRY")
        timezone = os.getenv("TIMEZONE")
        tools.append({
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": country,
                "timezone": timezone
            }
        })

    if file_search:
        people_vector_store = openai_utils.get_vector_store("people")
        journals_vector_store = openai_utils.get_vector_store("journals")
        tools.append({
            "type": "file_search",
            "vector_store_ids": [people_vector_store.id, journals_vector_store.id],
        })
        print(f"Using people (ID: {people_vector_store.id}) and journals (ID: {journals_vector_store.id}) for file search\n")

    return tools