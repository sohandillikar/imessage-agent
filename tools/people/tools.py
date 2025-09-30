from datetime import datetime
import tools.people.utils as people_utils

def add_liking_to_person(person_name: str, liking: str) -> str:
    """
    Add an interest or liking to someone's profile when you learn about it in conversation.
    Use this ONLY when someone explicitly expresses a genuine ongoing interest, hobby, passion, or preference.
    Do NOT use this for temporary experiences, situations, or activities they're currently engaged in.
    Args:
        person_name: The name of the person
        liking: A very specific liking to add. Do NOT use this function for generic likes
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    liking = liking.lower().strip()
    person = people_utils.find_person_by_name(person_name)
    if person is None:
        person = people_utils.create_new_person(person_name, likes=[liking])
    else:
        people = people_utils.get_people()
        for p in people:
            if p["id"] == person["id"]:
                p["likes"].append(liking)
                new_dislikes = people_utils.remove_similar_items(liking, p["dislikes"])
                if len(new_dislikes) < len(p["dislikes"]):
                    print(f"Removed {set(p['dislikes']) - set(new_dislikes)} from {person_name}'s dislikes")
                    p["dislikes"] = new_dislikes
                break
        people_utils.update_people(people)
    return "success"

def add_disliking_to_person(person_name: str, disliking: str) -> str:
    """
    Add a disliking to someone's profile when you learn about it in conversation.
    Use this ONLY when someone explicitly expresses a genuine ongoing dislike, aversion, or negative preference.
    Do NOT use this for temporary problems, inconveniences, or frustrations they're currently experiencing.
    Args:
        person_name: The name of the person
        disliking: A very specific disliking to add. Do NOT use this function for generic dislikes
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    disliking = disliking.lower().strip()
    person = people_utils.find_person_by_name(person_name)
    if person is None:
        person = people_utils.create_new_person(person_name, dislikes=[disliking])
    else:
        people = people_utils.get_people()
        for p in people:
            if p["id"] == person["id"]:
                p["dislikes"].append(disliking)
                new_likes = people_utils.remove_similar_items(disliking, p["likes"])
                if len(new_likes) < len(p["likes"]):
                    print(f"Removed {set(p['likes']) - set(new_likes)} from {person_name}'s likes")
                    p["likes"] = new_likes
                break
        people_utils.update_people(people)
    return "success"

def add_fact_to_person(person_name: str, fact: str) -> str:
    """
    Add a fact to someone's profile when you learn about it in conversation.
    Use this ONLY when you learn a fact about someone's life that should be remembered for future conversations.
    Do NOT use this to capture likes or dislikes. Use the add_liking_to_person or add_disliking_to_person functions instead, if appropriate.
    Args:
        person_name: The name of the person
        fact: A very specific fact to add. Do NOT use this function for generic facts
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    fact = fact.lower().strip()
    memory = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "memory": fact}
    person = people_utils.find_person_by_name(person_name)
    if person is None:
        person = people_utils.create_new_person(person_name, memories=[memory])
    else:
        people = people_utils.get_people()
        for p in people:
            if p["id"] == person["id"]:
                p["memories"].append(memory)
                break
        people_utils.update_people(people)
    return "success"

def call_function(name: str, args: dict):
    if name == "add_liking_to_person":
        return add_liking_to_person(**args)
    if name == "add_disliking_to_person":
        return add_disliking_to_person(**args)
    if name == "add_fact_to_person":
        return add_fact_to_person(**args)
    raise ValueError(f"Function 'people.{name}' not found")