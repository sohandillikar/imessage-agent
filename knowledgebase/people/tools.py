import knowledgebase.people.utils as people_utils

def get_user_email() -> str:
    """
    Get your email address.
    Use this when someone asks for your email or contact information.
    Returns:
        str: Email address
    """
    return people_utils.get_user_info()["email"]

def get_user_phone() -> str:
    """
    Get your phone number.
    Use this when someone asks for your phone number or contact information.
    Returns:
        str: Phone number
    """
    return people_utils.get_user_info()["phone"]

def get_user_background() -> dict[str, list[str]]:
    """
    Get information about your career, education, occupations, and history.
    Use this when someone asks about your job, career, education, or past experiences.
    Examples:
        - "What do you do?"
        - "What's your job?"
        - "Tell me about your work"
        - "What's your major?"
    Returns:
        dict: Occupations and history
    """
    user = people_utils.get_user_info()
    return {
        "occupations": user["occupations"],
        "history": user["history"]
    }

def get_user_interests() -> list[str]:
    """
    Get your interests and hobbies.
    Use this when someone asks you about what to do, planning activities, suggesting things, 
    or when you need to know your preferences for making decisions or recommendations.
    Examples:
        - "What should we do?",
        - "Any ideas?",
        - "What do you want to do?",
        - "Let's plan something"
    Returns:
        list: List of interests
    """
    return people_utils.get_user_info()["interests"]

def call_function(name: str, args: dict):
    if name == "get_user_email":
        return get_user_email(**args)
    if name == "get_user_phone":
        return get_user_phone(**args)
    if name == "get_user_background":
        return get_user_background(**args)
    if name == "get_user_interests":
        return get_user_interests(**args)
    raise ValueError(f"Function '{name}' not found")