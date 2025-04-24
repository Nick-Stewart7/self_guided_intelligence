# memory.py
import boto3, json, random

class MemorySystem:
    def __init__(self):
        random_integer = random.randint(1000, 2000)
        self.session_memory = {
            "chain_id": random_integer,
            "current_user_input": "",
            "conversation_history": [],
            "past_actions": [],
            "living_context": "",
            "journal":[],
            "next_directive": "",
            "keyframes": [],
            "unresolved_paths": []
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
        self.session_memory["living_context"] = observation["living_context"]
        self.session_memory["next_directive"] = observation["next_directive"]

    def store_action(self, action, step):
        self.session_memory["past_actions"].append({"step": step, "action": action})

    def store_reflection(self, reflection):
        self.session_memory["living_context"] = reflection["updated_living_context"]
        self.session_memory["journal"].append(reflection["journal_entry"])
        self.session_memory["keyframes"].append(reflection["keyframes"])
        return reflection