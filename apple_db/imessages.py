import os
import sqlite3
import subprocess
from datetime import date
from dotenv import load_dotenv
from dataclasses import dataclass
import apple_db.contacts as contacts
import apple_db.utils as apple_db_utils
import tools.people.utils as people_utils

from pprint import pprint

load_dotenv()

DB_PATH = os.getenv("IMESSAGES_DB_PATH")

@dataclass
class Message:
    dt: str
    guid: str
    reply_to_guid: str
    content: str
    sender_id: str
    chat_id: str
    chat_name: str
    is_from_me: int

def decode_attributed_body(body: bytes) -> str:
    content = body.decode("utf-8", errors="ignore")
    start_str = "NSString"
    start = content.find(start_str) + len(start_str)
    end = content.find("\x02iI")
    decoded_body = content[start:end]
    start_2 = decoded_body.find("+") + 1
    decoded_body = decoded_body[start_2:][1:].strip()
    return decoded_body

def get_messages(get_sender_info: bool = False, options: str = "") -> list[Message]:
    if options:
        options = f"AND {options}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"""
    SELECT
        datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as dt,
        m.guid,
        m.reply_to_guid,
        m.text,
        m.attributedBody,
        h.id as sender_id,
        c.chat_identifier as chat_id,
        c.display_name as chat_name,
        m.is_from_me
    FROM message m
    LEFT JOIN handle h ON m.handle_id = h.ROWID
    LEFT JOIN chat c ON m.cache_roomnames = c.chat_identifier
    WHERE (m.text IS NOT NULL OR m.attributedBody IS NOT NULL) {options}
    """
    cursor.execute(query)
    messages = cursor.fetchall()
    messages = apple_db_utils.sql_output_to_json(messages, cursor.description)
    for i, message in enumerate(messages):
        if message["text"] and message["text"].strip():
            messages[i]["content"] = message["text"]
        else:
            messages[i]["content"] = decode_attributed_body(message["attributedBody"])
        del messages[i]["text"]
        del messages[i]["attributedBody"]
        if get_sender_info:
            if message["is_from_me"] == 1:
                user = people_utils.get_user()
                messages[i]["sender_info"] = user
                messages[i]["sender_id"] = user["phone"]
            else:
                sender = people_utils.get_person_by_sender_id(message["sender_id"])
                if sender is None:
                    contacts_list = contacts.filter_contacts(phone=message["sender_id"], email=message["sender_id"])
                    if len(contacts_list) > 0:
                        sender = people_utils.create_new_person_from_contact(contacts_list[0])
                messages[i]["sender_info"] = sender
    cursor.close()
    conn.close()
    return messages

def get_unread_messages(get_sender_info: bool = False, options: str = "") -> list[Message]:
    if options:
        options = f"AND {options}"
    apple_reference_date = date(2001, 1, 1)
    today = date(2025, 9, 28) # date.today()
    diff_seconds = (today - apple_reference_date).total_seconds()
    diff_nanoseconds = int(diff_seconds * 1_000_000_000)
    options = f"m.date > {diff_nanoseconds} {options} AND m.is_read=0 and m.is_from_me=0"
    return get_messages(get_sender_info=get_sender_info, options=options)

def get_conversation_history(message: Message, get_sender_info: bool = False) -> tuple[list[Message], list[str]]:
    conversation_history = []
    current_message = message
    while True:
        options_query = f"m.guid = '{current_message['reply_to_guid']}'"
        earlier_message = get_messages(get_sender_info=get_sender_info, options=options_query)
        if len(earlier_message) > 0:
            earlier_message = earlier_message[0]
            conversation_history.insert(0, earlier_message)
            current_message = earlier_message
        else:
            break
    conversation_history.append(message)
    return conversation_history

def send_message(message: str, sender_id: str) -> None:
    script = f"""
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to participant "{sender_id}" of targetService
        send "{message}" to targetBuddy
    end tell
    """
    return subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)