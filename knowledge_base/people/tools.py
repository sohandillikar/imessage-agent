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
    new_liking = new_liking.lower().strip()
    person = people_utils.find_person_by_name(person_name)
    if person is None:
        person = people_utils.create_new_person(person_name, likes=[new_liking])
    else:
        people = people_utils.get_people()
        for p in people:
            if p["id"] == person["id"]:
                p["likes"].append(new_liking)
                new_dislikes = people_utils.remove_similar_items(new_liking, p["dislikes"])
                if len(new_dislikes) < len(p["dislikes"]):
                    print(f"Removed {set(p['dislikes']) - set(new_dislikes)} from {person_name}'s dislikes")
                    p["dislikes"] = new_dislikes
                break
        people_utils.update_people(people)
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
    new_disliking = new_disliking.lower().strip()
    person = people_utils.find_person_by_name(person_name)
    if person is None:
        person = people_utils.create_new_person(person_name, dislikes=[new_disliking])
    else:
        people = people_utils.get_people()
        for p in people:
            if p["id"] == person["id"]:
                p["dislikes"].append(new_disliking)
                new_likes = people_utils.remove_similar_items(new_disliking, p["likes"])
                if len(new_likes) < len(p["likes"]):
                    print(f"Removed {set(p['likes']) - set(new_likes)} from {person_name}'s likes")
                    p["likes"] = new_likes
                break
        people_utils.update_people(people)
    return "success"

def call_function(name: str, args: dict):
    if name == "add_new_liking_to_person":
        return add_new_liking_to_person(**args)
    if name == "add_new_disliking_to_person":
        return add_new_disliking_to_person(**args)
    raise ValueError(f"Function 'people.{name}' not found")