import os
import json
import utils
import sqlite3
from dataclasses import dataclass

# SETTINGS
USER = "sohan"
DB_PATH = f"/Users/{USER}/Library/Messages/chat.db"

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

def get_contacts(options: str = '') -> list[dict]:
    if options:
        options = f"WHERE {options}"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM handle {options}"
    cursor.execute(query)
    
    contacts = cursor.fetchall()
    contacts = utils.sql_output_to_json(contacts, cursor.description)

    cursor.close()
    conn.close()

    return contacts

def get_messages(options: str = '') -> list[Message]:
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
    messages = utils.sql_output_to_json(messages, cursor.description)

    for i, message in enumerate(messages):
        if message['text'] and message['text'].strip():
            messages[i]['content'] = message['text']
        else:
            messages[i]['content'] = decode_attributed_body(message['attributedBody'])
        
        del messages[i]['text']
        del messages[i]['attributedBody']

    cursor.close()
    conn.close()

    return messages

def get_conversation_history(message: Message, clean: bool = False, bad_messages_file: str = 'bad_messages.json') -> tuple[list[Message], list[str]]:
    if os.path.exists(bad_messages_file):
        with open(bad_messages_file, 'r') as f:
                bad_messages = json.load(f)
    else:
        bad_messages = {}
    
    conversation_history = []
    ignore_guids = []
    current_message = message
    
    while True:
        options_query = f"m.guid = '{current_message['reply_to_guid']}'"
        earlier_message = get_messages(options=options_query)
        if len(earlier_message) > 0:
            earlier_message = earlier_message[0]
            if clean and earlier_message['guid'] in bad_messages:
                earlier_message['content'] = bad_messages[earlier_message['guid']]['rephrased']
                if len(earlier_message['content']) > 0:
                    conversation_history.insert(0, earlier_message)
                else:
                    ignore_guids.append(earlier_message['guid'])
            else:
                conversation_history.insert(0, earlier_message)
            current_message = earlier_message
        else:
            break
    
    if clean and message['guid'] in bad_messages:
        message['content'] = bad_messages[message['guid']]['rephrased']
        if len(message['content']) > 0:
            conversation_history.append(message)
        else:
            ignore_guids.append(message['guid'])
    else:
        conversation_history.append(message)
    
    return conversation_history, ignore_guids

def get_conversations(messages: list[Message], unique: bool = True, clean: bool = False, bad_messages_file: str = 'bad_messages.json') -> list[list[Message]]:
    """
    messages: list of messages from oldest to newest
    """
    convos = []
    all_ignore_guids = []

    def is_message_in_convos(message):
        for convo in convos:
            for convo_message in convo:
                if message['guid'] == convo_message['guid']:
                    return True
        return False

    for i in range(len(messages) - 1, -1, -1):
        if not messages[i]['guid'] in all_ignore_guids and ((not unique) or (unique and not is_message_in_convos(messages[i]))):
            convo, ignore_guids = get_conversation_history(messages[i], clean, bad_messages_file)
            all_ignore_guids.extend(ignore_guids)
            convos.append(convo)

    return convos

def prepare_convo_for_fine_tuning(convo: list[Message], system_prompt: str) -> dict:
    while len(convo) > 0 and convo[0]["is_from_me"]:
        del convo[0]
    if not convo: return None

    fine_tuning_data = [{"role": "system", "content": system_prompt}]

    for message in convo:
        role = "assistant" if message["is_from_me"] else "user"
        fine_tuning_data.append({"role": role, "content": message["content"]})

    return {"messages": fine_tuning_data}

def prepare_convos_for_fine_tuning(convos: list[list[Message]], system_prompt: str, output_file: str, indent: int = None):
    with open(output_file, 'w') as f:
        for convo in convos:
            fine_tuning_data = prepare_convo_for_fine_tuning(convo, system_prompt)
            if not fine_tuning_data is None:
                f.write(json.dumps(fine_tuning_data, indent=indent) + '\n')