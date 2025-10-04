import os
from dotenv import load_dotenv
import tools.people.utils as people_utils
import tools.journals.utils as journals_utils
import tools.messages.utils as messages_utils
import tools.gcal.utils as gcal_utils

load_dotenv()

# Give full disk access to Terminal or IDE
# Give location permissions to Python

def setup(update_vector_stores: bool = True) -> None:
    env_vars = ["IMESSAGES_DB_PATH", "CONTACTS_DB_PATH", "OPENAI_API_KEY", "COUNTRY", "TIMEZONE"]
    for env_var in env_vars:
        if not os.getenv(env_var):
            raise ValueError(f"{env_var} is not set in .env")

    if update_vector_stores:
        people_utils.update_people()
        journals_utils.load_journals()
        messages_utils.load_messages()

    calendar = gcal_utils.get_calendar_by_name("iMessage Agent")
    if calendar is None:
        print("WARNING: No calendar found for iMessage Agent. Creating one...")
        calendar = gcal_utils.create_calendar("iMessage Agent", "A calendar for events created by your iMessage Agent.")
        print(f"Created calendar: {calendar['summary']}")

if __name__ == "__main__":
    setup()