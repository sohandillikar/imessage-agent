import os
import sys
import json
from rapidfuzz import process

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import openai_utils

def get_people() -> list[dict]:
    with open(f"knowledge_base/people.json", "r") as f:
        return json.load(f)

def update_people(people: list[dict]) -> None:
    with open(f"knowledge_base/people.json", "w") as f:
        json.dump(people, f, indent=4)
    openai_utils.update_knowledge_base(data_file_paths=["knowledge_base/people.json"])

def create_new_person(
    full_name: str,
    gender: str = None,
    email: str = None,
    phone: str = None,
    nicknames: list[str] = [],
    relations: list[str] = [],
    occupations: list[str] = [],
    history: list[str] = [],
    likes: list[str] = [],
    dislikes: list[str] = [],
    memories: list[dict] = []) -> dict:
    people = get_people()
    person_id = max([person["id"] for person in people]) + 1
    people.append({
        "id": person_id,
        "full_name": full_name,
        "gender": gender,
        "email": email,
        "phone": phone,
        "nicknames": nicknames,
        "relations": relations,
        "occupations": occupations,
        "history": history,
        "likes": likes,
        "dislikes": dislikes,
        "memories": memories
    })
    update_people(people)
    return people[-1]

def get_user_info() -> dict | None:
    people = get_people()
    for person in people:
        if "self" in person["relations"]:
            return person
    print("WARNING: No user info found in knowledge_base/people.json")
    return None

def get_person_info_by_sender_id(sender_id: str) -> dict | None:
    people = get_people()
    for person in people:
        if person["phone"] == sender_id or person["email"] == sender_id:
            return person
    return None

def find_person_by_name(name: str) -> dict | None:
    name = name.lower().strip()
    people = get_people()
    all_names = {}
    for person in people:
        all_names[person["full_name"].lower().strip()] = person
        for nickname in person["nicknames"]:
            all_names[nickname.lower().strip()] = person
    match = process.extractOne(name, all_names.keys())
    if match[1] >= 90:
        return all_names[match[0]]
    return None

def remove_similar_items(target: str, items: list[str], score_cutoff: int = 70) -> list[str]:
    items = [item.lower().strip() for item in items]
    matches = process.extract(target, items, score_cutoff=score_cutoff)
    matches = [match[0] for match in matches]
    filtered_items = [item for item in items if item not in matches]
    return filtered_items