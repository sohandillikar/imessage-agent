import knowledge_base.people.utils as people_utils

def add_new_liking_to_person(person_name: str, new_liking: str) -> str:
    """
    Add a new interest or liking to someone's profile when you learn about it in conversation.
    Use this when someone mentions any new hobby, interest, passion, or liking they have.
    Args:
        person_name: The name of the person
        new_liking: Their new liking to add
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    print(f"Adding liking {new_liking} to {person_name}")
    return "success"

def add_new_disliking_to_person(person_name: str, new_disliking: str) -> str:
    """
    Add a new disliking to someone's profile when you learn about it in conversation.
    Use this when someone mentions something they don't like, hate, or want to avoid.
    Args:
        person_name: The name of the person
        new_disliking: Their new disliking to add
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    print(f"Adding disliking {new_disliking} to {person_name}")
    return "success"

def call_function(name: str, args: dict):
    if name == "add_new_liking_to_person":
        return add_new_liking_to_person(**args)
    if name == "add_new_disliking_to_person":
        return add_new_disliking_to_person(**args)
    raise ValueError(f"Function 'people.{name}' not found")