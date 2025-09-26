# memory.py
import boto3
from self_guided_ai.config.config import config

class MemorySystem:
    def __init__(self):
        self.session_memory = {
            "conversation_history": [],
            "past_actions": [],
            "current_objective": "",
            "journal": [],
            "plan": [],
            "commitments": [],
            "open_questions": [],
            "artifacts": ["scratchpad.md"],
            "emotional_state": config.aria.initial_emotional_state.copy(),
            "meta_analysis": ""
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
    
    def store_observation(self, observation):
        """Store observation data with error handling"""
        try:
            self.session_memory["plan"] += observation.get("plan", [])
            self.session_memory["current_objective"] = observation.get("current_objective", "No current objective defined")
            self.session_memory["emotional_state"] = observation.get("emotional_state", {})
            self.session_memory["open_questions"] = observation.get("open_questions", [])
            
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error storing observation: {e}")

    def store_action(self, action):
        self.session_memory["past_actions"].append(action)
        working_list = self.session_memory["past_actions"]
        if len(working_list) >= 10:
            working_list.pop(0)  # Maintain a max of 10 past actions
            self.session_memory["past_actions"] = working_list
        

    def store_reflection(self, reflection):
        """Store reflection data with error handling"""
        try:
            self.session_memory["current_objective"] = reflection.get("next_objective", self.session_memory.get("current_objective", "No current objective defined"))
            self.session_memory["journal"].append(reflection.get("journal_entry", "Error extracting journal entry"))
            self.session_memory["emotional_state"] = reflection.get("emotional_state", {})
            self.session_memory["meta_analysis"] = reflection.get("meta_analysis", "")
            self.session_memory["commitments"] = reflection.get("commitments", [])
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error storing reflection: {e}")
            # Ensure we don't break the system
            self.session_memory["journal"].append(f"Error storing reflection: {str(e)}")

    def store_artifact(self, artifact_path):
        if artifact_path not in self.session_memory["artifacts"]:
            self.session_memory["artifacts"].append(artifact_path)