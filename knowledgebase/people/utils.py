import os
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

def get_person_info(sender_id: str) -> dict:
    people = get_people()
    for person in people:
        if person["phone"] == sender_id or person["email"] == sender_id:
            return person
    return None