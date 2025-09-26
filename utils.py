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