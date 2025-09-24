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

def get_person_email(person_name: str) -> str:
    """
    Get the email address of anyone in your social circle.
    Use this when someone asks for the email or contact information of a person.
    Args:
        person_name: The name of the person
    Returns:
        dict: Email information with status:
        - {"status": "found", "email": "email@example.com"} if email found
        - {"status": "multiple_found", "people": ["Name1", "Name2"]} if multiple people with same name
        - {"status": "not_found"} if no person found or no email available
    """
    people = people_utils.filter_people_by_name(person_name)
    if len(people) == 1 and people[0]["email"] is not None:
        return {"status": "found", "email": people[0]["email"]}
    if len(people) > 1:
        return {"status": "multiple_found", "people": [p["full_name"] for p in people]}
    return {"status": "not_found"}

def call_function(name: str, args: dict):
    if name == "get_user_email":
        return get_user_email(**args)
    if name == "get_user_phone":
        return get_user_phone(**args)
    if name == "get_user_background":
        return get_user_background(**args)
    if name == "get_user_interests":
        return get_user_interests(**args)
    if name == "get_person_email":
        return get_person_email(**args)
    raise ValueError(f"Function '{name}' not found")