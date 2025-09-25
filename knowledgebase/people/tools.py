import knowledgebase.people.utils as people_utils

avoid_functions = ["call_function"]

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

def add_contact_info(person_name: str, info_type: str, info_value: str) -> dict:
    """
    Add new contact information when you learn about it.
    Use this when someone mentions a new phone number, email, or social media handle.
    
    Args:
        person_name: The name of the person
        info_type: Type of info ("phone", "email", "instagram", etc.)
        info_value: The actual contact information
    
    Returns:
        dict: Status of the update operation
    """
    # Implementation to update people.json
    pass

def add_background_info(person_name: str, new_info: str) -> dict:
    """
    Add new background information about someone.
    Use this when you learn new facts about someone's life, job, or experiences.
    
    Args:
        person_name: The name of the person
        new_info: The new background information to add
    
    Returns:
        dict: Status of the update operation
    """
    # Implementation to update people.json
    pass

def call_function(name: str, args: dict):
    if name == "add_new_liking_to_person":
        return add_new_liking_to_person(**args)
    if name == "add_new_disliking_to_person":
        return add_new_disliking_to_person(**args)
    raise ValueError(f"Function '{name}' not found")