import json

def get_people() -> list[dict]:
    with open(f"knowledgebase/people/people.json", "r") as f:
        return json.load(f)

def get_user_info() -> dict:
    people = get_people()
    for person in people:
        if "self" in person["relations"]:
            return person
    print("WARNING: No user info found in knowledgebase/people/people.json!")
    return None

def get_person_info_by_sender_id(sender_id: str) -> dict:
    people = get_people()
    for person in people:
        if person["phone"] == sender_id or person["email"] == sender_id:
            return person
    return None

def filter_people_by_name(name: str) -> list[dict]:
    people = get_people()
    name = name.lower().strip()
    filtered_people = []
    for person in people:
        if name in person["full_name"].lower().strip():
            filtered_people.append(person)
    return filtered_people