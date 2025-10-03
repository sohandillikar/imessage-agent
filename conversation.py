import os
import openai_utils
from base64 import b64encode
import apple_db.imessages as imessages
import tools.people.utils as people_utils

class Conversation:
    def __init__(self, message: imessages.Message, max_context_length: int = None, tools: list[dict] = []):
        self.max_context_length = max_context_length
        self.tools = tools
        self.person1 = people_utils.get_user()
        self.person2 = message["sender_info"]
        self.person2_id = message["sender_id"]
        self.system_prompt = openai_utils.create_system_prompt(sender_id=message["sender_id"])
        self.imessage_history = imessages.get_conversation_history(message, get_sender_info=True, max_length=max_context_length)
        self.llm_history = self._convert_imessage_convo_for_llm(self.imessage_history, include_system_prompt=True)
        print(f"System prompt: {self.system_prompt}")

    def _encode_file(self, file_path: str) -> str:
        file_path = os.path.expanduser(file_path)
        with open(file_path, "rb") as f:
            return b64encode(f.read()).decode("utf-8")

    def _is_acceptable_mime_type(self, mime_type: str) -> bool:
        if not mime_type:
            return False
        mime_type = mime_type.lower().strip()
        _type = mime_type.split("/")[0]
        acceptable_mime_types = ["image/jpg", "image/jpeg", "image/png", "image/gif", "image/webp", "application/pdf"]
        acceptable_types = [] # TODO: Add "text"
        return mime_type in acceptable_mime_types or _type in acceptable_types

    def _is_acceptable_attachment(self, message: imessages.Message) -> bool:
        return message["filename"] is not None and message["is_sticker"] == 0 and self._is_acceptable_mime_type(message["mime_type"])

    def _convert_imessage_convo_for_llm(self, imessage_convo: list[imessages.Message], include_system_prompt: bool = False) -> list[dict]:
        if include_system_prompt:
            llm_convo = [{"role": "system", "content": [{"type": "input_text", "text": self.system_prompt}]}]
        else:
            llm_convo = []
        person2_first_name = self.person2["full_name"].split(" ")[0]
        for message in imessage_convo:
            content = message["content"]
            if message["is_from_me"] == 0:
                llm_convo.append({
                    "role": "user",
                    "content": [{
                        "type": "input_text",
                        "text": f"{person2_first_name}: {content}"
                    }]
                })
                if self._is_acceptable_attachment(message):
                    attachement_encoded = self._encode_file(message["filename"])
                    attachment_type = "image" if "image" in message["mime_type"] else "file"
                    attachment_tag = "image_url" if attachment_type == "image" else "file_data"
                    attachment_content = {
                        "type": f"input_{attachment_type}",
                        attachment_tag: f"data:{message['mime_type']};base64,{attachement_encoded}"
                    }
                    if attachment_type == "file":
                        attachment_content["filename"] = os.path.basename(message["filename"])
                    llm_convo[-1]["content"].insert(0, attachment_content)
            else:
                llm_convo.append({
                    "role": "assistant",
                    "content": [{
                        "type": "output_text",
                        "text": content
                    }]
                })
        return llm_convo

    def _trim_conversation(self):
        if self.max_context_length and len(self.llm_history) > self.max_context_length:
            self.llm_history = self.llm_history[-self.max_context_length:]
            self.llm_history.insert(0, {"role": "system", "content": [{"type": "input_text", "text": self.system_prompt}]})
            print(f"Conversation trimmed to {self.max_context_length} messages")

    def _add_to_conversation_history(self, new_imessages: list[imessages.Message]):
        self.imessage_history.extend(new_imessages)
        llm_messages = self._convert_imessage_convo_for_llm(new_imessages)
        self.llm_history.extend(llm_messages)
        # self._trim_conversation() # TODO: Properly trim conversation history

    def check_for_new_messages(self):
        unread_messages = imessages.get_unread_messages(get_sender_info=True, group_chats=False, options=f"sender_id='{self.person2_id}'")
        new_messages = []
        current_message_ids = [m["guid"] for m in self.imessage_history]
        for message in unread_messages:
            if message["guid"] not in current_message_ids:
                new_messages.append(message)
        if len(new_messages) > 0:
            self._add_to_conversation_history(new_messages)
        return new_messages
    
    def respond(self):
        self.print_conversation()
        response, self.llm_history = openai_utils.create_response(self.llm_history, tools=self.tools)
        # self._trim_conversation() # TODO: Properly trim conversation history
        print(f"Response: {response.output_text} ({response.usage.total_tokens} tokens)")
        send_permission = input(f"Send response? (y/n): ")
        if send_permission == "y":
            imessages.send_message(response.output_text, sender_id=self.person2_id)
        return response

    def print_conversation(self, max_messages: int = 10):
        conversation = self.imessage_history
        if len(conversation) > max_messages:
            conversation = conversation[-max_messages:]
        for message in conversation:
            if message["is_from_me"] == 1:
                print(f"{self.person1['full_name']}: {message['content']}")
            else:
                print(f"{self.person2['full_name']}: {message['content']}")