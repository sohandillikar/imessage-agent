import subprocess
import json

def send_imessage(phone_number, message):
    """
    Send an iMessage using AppleScript
    """
    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to participant "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return {"success": True, "message": "Message sent successfully"}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}

# Usage
result = send_imessage("4083388934", "Hello again!")
print(result)