import os
import sys
import json
import glob
from dotenv import load_dotenv
from datetime import datetime
from emoji import replace_emoji
import tools.people.utils as people_utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import openai_utils

load_dotenv()

def get_journals() -> list[dict]:
    with open(f"knowledge_base/journals.json", "r") as f:
        return json.load(f)

def update_journals(journals: list[dict]) -> None:
    with open(f"knowledge_base/journals.json", "w") as f:
        json.dump(journals, f, indent=4)
    vector_store = openai_utils.get_vector_store("knowledge_base")
    openai_utils.update_vector_store(vector_store, ["knowledge_base/journals.json"])

def parse_entry(entry_lines: list[str]) -> list[dict]:
    rosebud_username = os.getenv("ROSEBUD_USERNAME")
    user = people_utils.get_user()
    entry = "\n".join([line for line in entry_lines if line])
    entries = [e for e in entry.split("**Rosebud:**") if e]
    for i in range(len(entries)):
        question, answer = entries[i].split(f"**{rosebud_username}:**", 1)
        questions = question.split("\n")
        for j in range(len(questions) - 1, -1, -1):
            question = replace_emoji(questions[j]).strip()
            if question and question.endswith("?"):
                break
        answer = f"{user['full_name']}: {replace_emoji(answer).strip()}"
        entries[i] = {"question": question, "answer": answer}
    return entries

def parse_journal(file_path: str) -> dict:
    with open(file_path, "r") as f:
        content = f.read()
    lines = content.split("\n")
    
    title = None
    date_formatted = None
    emotions = []
    people = []
    topics = []
    entries = []

    for i, line in enumerate(lines):
        if line.startswith("##") and title is None:
            title = replace_emoji(line.replace("##", "")).strip()
        elif line.startswith("###") and date_formatted is None:
            date_formatted = line.replace("###", "").strip()
        elif line.startswith("**Emotions:**"):
            emotions = line.replace("**Emotions:**", "").strip().split(",")
            emotions = [e.strip() for e in emotions]
        elif line.startswith("**People:**"):
            people = line.replace("**People:**", "").strip().split(",")
            people = [p.strip() for p in people]
        elif line.startswith("**Topics:**"):
            topics = line.replace("**Topics:**", "").strip().split(",")
            topics = [t.strip() for t in topics]
        elif line.strip() == "#### Entry":
            entries = parse_entry(lines[i+1:])
            break

    return {
        "title": title,
        "date_formatted": date_formatted,
        "emotions": emotions,
        "people": people,
        "topics": topics,
        "entries": entries
    }

def load_journals(new_only: bool = False) -> list[dict]:
    journals = get_journals()
    journal_dates = [j["date"] for j in journals]
    journal_file_paths = glob.glob("knowledge_base/rosebud_entries/rosebud-entry-*.md")

    for file_path in journal_file_paths:
        file_name = os.path.basename(file_path)
        file_date = file_name.replace("rosebud-entry-", "").replace(".md", "")
        file_date = datetime.strptime(file_date, "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%d %H:%M:%S")
        if file_date not in journal_dates or not new_only:
            journal = parse_journal(file_path)
            journal["date"] = file_date
            journals.append(journal)
    
    update_journals(journals)
    return journals