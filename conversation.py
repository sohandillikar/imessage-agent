import openai_utils
from setup import setup
import apple_db.imessages as imessages

from pprint import pprint

client = setup(update_knowledge_base=False)

class Conversation:
    def __init__(self, message: imessages.Message, max_length: int = 20, tools: list[dict] = []):
        self.max_length = max_length
        self.tools = tools
        self.person2 = message["sender_info"]
        self.person2_id = message["sender_id"]
        self.system_prompt = openai_utils.create_system_prompt(sender_id=message["sender_id"])
        self.imessage_history = imessages.get_conversation_history(message, get_sender_info=True, max_length=max_length)
        self.llm_history = self.convert_imessage_convo_for_llm(self.imessage_history)
        print(f"System prompt: {self.system_prompt}")

    def convert_imessage_convo_for_llm(self, imessage_convo: list[imessages.Message]) -> list[dict]:
        llm_convo = [{"role": "system", "content": [{"type": "input_text", "text": self.system_prompt}]}]
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
            else:
                llm_convo.append({
                    "role": "assistant",
                    "content": [{
                        "type": "output_text",
                        "text": content
                    }]
                })
        return llm_convo

    def trim_conversation(self):
        if len(self.llm_history) > self.max_length:
            self.llm_history = self.llm_history[-self.max_length:]
            self.llm_history.insert(0, {"role": "system", "content": [{"type": "input_text", "text": self.system_prompt}]})
            print(f"Conversation trimmed to {self.max_length} messages")

    def add_to_conversation_history(self, new_imessages: list[imessages.Message]):
        self.imessage_history.extend(new_imessages)
        llm_messages = self.convert_imessage_convo_for_llm(new_imessages)
        self.llm_history.extend(llm_messages)
        self.trim_conversation()

    def check_for_new_messages(self):
        unread_messages = imessages.get_unread_messages(get_sender_info=True, options=f"sender_id='{self.person2_id}'")
        new_messages = []
        current_message_ids = [m["guid"] for m in self.imessage_history]
        for message in unread_messages:
            if message["guid"] not in current_message_ids:
                new_messages.append(message)
        if len(new_messages) > 0:
            self.add_to_conversation_history(new_messages)
        return new_messages

    def respond(self):
        response, self.llm_history = openai_utils.create_response(client, self.llm_history, tools=self.tools)
        self.trim_conversation()

        print(f"Response: {response.output_text} ({response.usage.total_tokens} tokens)")
        send_permission = input(f"Send response? (y/n): ")
        if send_permission == "y":
            imessages.send_message(response.output_text, sender_id=self.person2_id)
        
        return response
