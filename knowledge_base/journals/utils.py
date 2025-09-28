import os
import json
import glob
from datetime import datetime
from emoji import replace_emoji

def get_journals() -> list[dict]:
    with open(f"knowledge_base/journals/journals.json", "r") as f:
        return json.load(f)

def update_journals(journals: list[dict]) -> None:
    with open(f"knowledge_base/journals/journals.json", "w") as f:
        json.dump(journals, f, indent=4)
    # openai_utils.update_knowledge_base(data_file_paths=["knowledge_base/journals/journals.json"])

def parse_journal(file_path: str) -> dict:
    with open(file_path, "r") as f:
        content = f.read()
    
    title = None
    date_formatted = None
    emotions = []
    people = []
    topics = []
    entries = []
    reading_entry = False

    for line in content.split("\n"):
        if line.strip() == "#### Entry":
            reading_entry = True
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
        elif line.startswith("**Rosebud:**"):
            question = replace_emoji(line.replace("**Rosebud:**", "")).strip()
            entries.append({"question": question})
        elif line.startswith("**") and reading_entry:
            answer = replace_emoji(line.split(":**", 1)[1]).strip()
            entries[-1]["answer"] = answer

    return {
        "title": title,
        "date_formatted": date_formatted,
        "emotions": emotions,
        "people": people,
        "topics": topics,
        "entries": entries
    }

def load_journals(new_only: bool = True) -> list[dict]:
    journals = get_journals()
    journal_dates = [j["date"] for j in journals]
    journal_file_paths = glob.glob("knowledge_base/journals/rosebud_entries/rosebud-entry-*.md")

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