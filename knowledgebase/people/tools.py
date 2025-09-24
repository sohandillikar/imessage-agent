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

def get_user_interests() -> list[str]:
    """
    Get your interests and hobbies.
    Use this when someone asks you about what to do, planning activities, suggesting things, 
    or when you need to know your preferences for making decisions or recommendations.
    Examples: "What should we do?", "Any ideas?", "What do you want to do?", "Let's plan something"
    Returns:
        list: List of interests
    """
    return people_utils.get_user_info()["interests"]