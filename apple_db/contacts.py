import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from dataclasses import dataclass
import apple_db.utils as utils
import tools.people.utils as people_utils
import tools.messages.utils as messages_utils

load_dotenv()

DB_PATH = os.getenv("CONTACTS_DB_PATH")

@dataclass
class Contact:
    id: str
    firstname: str
    lastname: str
    phone: str
    email: str

def normalize_phone(phone: str) -> str:
    try:
        return ''.join(filter(str.isdigit, phone))
    except:
        return None

def get_contacts(options: str = "") -> list[Contact]:
    if options:
        options = f"AND {options}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"""
    SELECT DISTINCT
        r.Z_PK as id,
        r.ZFIRSTNAME as firstname,
        r.ZLASTNAME as lastname,
        p.ZFULLNUMBER as phone,
        e.ZADDRESS as email
    FROM ZABCDRECORD r
    LEFT JOIN ZABCDPHONENUMBER p ON r.Z_PK = p.ZOWNER
    LEFT JOIN ZABCDEMAILADDRESS e ON r.Z_PK = e.ZOWNER
    WHERE r.ZFIRSTNAME IS NOT NULL AND
        (p.ZFULLNUMBER IS NOT NULL OR e.ZADDRESS IS NOT NULL) {options}
    """
    cursor.execute(query)
    contacts = cursor.fetchall()
    contacts = utils.sql_output_to_json(contacts, cursor.description)
    for contact in contacts:
        contact['phone'] = normalize_phone(contact['phone'])
    cursor.close()
    conn.close()
    return contacts

def filter_contacts(contacts: list[Contact] = None, firstname: str = None, lastname: str = None, \
                    phone: str = None, email: str = None, return_type: str = "json") -> list[Contact] | pd.DataFrame:
    if contacts is None:
        contacts = get_contacts()
    if phone:
        phone = normalize_phone(phone)
        phone = phone[1:] if len(phone) > 10 else phone
    if email and "@" not in email:
        email = None
    contacts = pd.DataFrame(contacts)
    filtered_contacts = contacts[
        (contacts["firstname"].str.contains(firstname, case=False, na=False) if firstname else True) &
        (contacts["lastname"].str.contains(lastname, case=False, na=False) if lastname else True) &
        (contacts["phone"].str.contains(phone, case=False, na=False) if phone else True) &
        (contacts["email"].str.contains(email, case=False, na=False) if email else True)
    ]
    if return_type == "json":
        return filtered_contacts.to_dict('records')
    return filtered_contacts

def setup_profiles():
    permissions = messages_utils.get_permissions()
    for sender_id in permissions.keys():
        sender = people_utils.get_person_by_sender_id(sender_id)
        if sender is None:
            contacts_list = filter_contacts(phone=sender_id, email=sender_id)
            if len(contacts_list) > 0:
                sender = people_utils.create_new_person_from_contact(contacts_list[0], sender_id=sender_id)
                print(f"Created new profile for {sender['full_name']} ({sender_id})\n")