# memory.py
import boto3

class MemorySystem:
    def __init__(self):
        self.session_memory = {
            "conversation_history": [],
            "past_actions": [],
            "current_context": "",
            "next_directive": "",
            "journal": []
        }
        self.long_term_memory_api = boto3.client("s3")  # Replace with actual AWS API
    
    def get_context(self):
        context = ""
        for reply in self.session_memory["conversation_history"]:
            if reply["role"] == "user":
                context += f"<|start_header_id|>user<|end_header_id|>\n{ reply['content'] }<|eot_id|>"
            elif reply["role"] == "AI":
                context += f"<|start_header_id|>assistant<|end_header_id|>\n {reply['content']}<|eot_id|>"
        return context
    
    def store_context(self, user_input, response):
        self.session_memory["conversation_history"].append({"role": "user", "content": user_input})
        self.session_memory["conversation_history"].append({"role": "AI", "content": response}) 
    
    def store_observation(self, observation, step):
        self.session_memory["past_actions"].append({"step": step, "action": "observation"})
        self.session_memory["current_context"] = observation["current_context"]
        self.session_memory["next_directive"] = observation["next_directive"]

    def store_action(self, action, step):
        self.session_memory["past_actions"].append({"step": step, "action": action})

    def store_reflection(self, reflection):
        self.session_memory["current_context"] = reflection["updated_context"]
        self.session_memory["journal"].append(reflection["journal_entry"])
        self.session_memory["next_directive"] = reflection["next_directive"]
        return reflection