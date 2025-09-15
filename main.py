import sqlite3
from pprint import pprint

def sql_output_to_json(output, columns):
    for i, row in enumerate(output):
        output[i] = {columns[j][0] : row[j] for j in range(len(columns))}
    return output

def decode_attributed_body(hex_string):
    """Decode attributedBody hex string to readable text"""
    binary_data = bytes.fromhex(hex_string)
    content = binary_data.decode('utf-8', errors='ignore')

    start_str = "NSString"
    start = content.find(start_str) + len(start_str)
    end = content.find("\x02iI")
    decoded_body = content[start:end]

    start_2 = decoded_body.find("+") + 1
    decoded_body = decoded_body[start_2:][1:].strip()

    return decoded_body

def get_messages(user, options=''):
    if options:
        options = f"AND {options}"
    
    db_path = f"/Users/{user}/Library/Messages/chat.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = f"""
    SELECT
        datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as dt,
        m.ROWID as message_id,
        m.text,
        hex(m.attributedBody) as body,
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
    messages = sql_output_to_json(messages, cursor.description)

    for i, message in enumerate(messages):
        if message['text'] and message['text'].strip():
            messages[i]['content'] = message['text']
            messages[i]['content_type'] = "plain_text"
        else:
            decoded_body = decode_attributed_body(message['body'])
            messages[i]['content'] = decoded_body
            messages[i]['content_type'] = "rich_text"
        
        del messages[i]['text']
        del messages[i]['body']

    cursor.close()
    conn.close()

    return messages

query_options = "dt >= '2025-09-14' AND dt < '2025-09-15'"
messages = get_messages("sohan", options=query_options) # Change this to your Mac username

pprint(messages)
print(len(messages))