import sys
from step1 import SENDER_ID, QUERY_OPTIONS, BAD_MESSAGES_FILE

sys.path.append('..')
import imessages as im

# SETTINGS
UNIQUE_CONVOS = False
CLEAN_CONVOS = True
SYSTEM_PROMPT = "You are Sohan's texting bot. Your job is to reply exactly as Sohan would text his girlfriend, Ishani. If Ishani sends multiple texts in a row, you may also reply with multiple texts if needed. Never break character and always respond like Sohan texting his girlfriend."
OUTPUT_FILE = "fine_tuning_data.jsonl"

def main():
    messages = im.get_messages(options=QUERY_OPTIONS)
    print(f"Found {len(messages)} messages sent by you to {SENDER_ID} w/ a reply_to_guid.")

    convos = im.get_conversations(
        messages,
        unique=UNIQUE_CONVOS,
        clean=CLEAN_CONVOS,
        bad_messages_file=BAD_MESSAGES_FILE
    )
    print(f"Found {len(convos)} convos.")

    im.prepare_convos_for_fine_tuning(convos, SYSTEM_PROMPT, output_file=OUTPUT_FILE)
    print(f"Done! Fine-tuning data is saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()