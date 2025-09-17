import os
import sys
import json
from datetime import datetime

sys.path.append('..')
import imessages as im

# SETTINGS
SENDER_ID = "+15107503277" # example: "+1XXXXXXXXXX"
QUERY_OPTIONS = f"""
sender_id = '{SENDER_ID}' AND
reply_to_guid IS NOT NULL AND
is_from_me = 1
"""
MANUAL_REPHRASE = False
BAD_MESSAGES_FILE = "bad_messages.json"
BAD_WORDS = [
    # Racial slurs
    "nigga", "nigger", "chink",
    
    # Slurs targeting sexuality / gender
    "fag", "faggot", "tranny", "shemale", "homo",
    
    # Slurs targeting disability / mental health
    "retard", "sped", "autistic",
    
    # General profanity
    "bitch", "slut", "whore", "cunt", "fuck", "shit",

    # Adult / sexual / violent terms
    "sex", "porn", "erotic", "hentai", "nude", "naked",
    "boobs", "tits", "ass", "dick", "cock", "pussy",
    "orgasm", "cum", "jerk off", "jack off", "masturbate",
    "masturbation", "condom", "rape", "rapist", "raping",
    "kill",
]

def extract_bad_messages(convos: list[im.Message], manual_rephrase: bool = True, output_file: str = None):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            bad_messages = json.load(f)
    else:
        bad_messages = {}

    new_bad_messages = 0

    for convo in convos:
        for message in convo:
            for word in BAD_WORDS:
                if not message['guid'] in bad_messages and message['content'].lower().find(word) != -1:
                    bad_messages[message['guid']] = {
                        'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'bad_word': word,
                        'is_from_me': message['is_from_me'],
                        'content': message['content'],
                        'rephrased': message['content'] if manual_rephrase else ''
                    }
                    new_bad_messages += 1

    print(f"Found {new_bad_messages} new bad messages.")
    
    if not output_file is None:
        with open(output_file, 'w') as f:
            json.dump(bad_messages, f, indent=4)
        print(f"Saved {len(bad_messages)} bad messages to {output_file}.")
    
    return bad_messages

QUERY_OPTIONS = f"""
sender_id = '{SENDER_ID}' AND
reply_to_guid IS NOT NULL AND
is_from_me = 1
"""

def main():
    messages = im.get_messages(options=QUERY_OPTIONS)
    print(f"Found {len(messages)} messages sent by you to {SENDER_ID} w/ a reply_to_guid.")

    convos = im.get_conversations(messages, unique=True, clean=False)
    print(f"Found {len(convos)} unique convos.")

    extract_bad_messages(convos, manual_rephrase=MANUAL_REPHRASE, output_file=BAD_MESSAGES_FILE)
    print("Done! Please review and rephrase all the new bad messages.")

if __name__ == "__main__":
    main()