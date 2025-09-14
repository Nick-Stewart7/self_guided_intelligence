# memory.py
import boto3
from config import config

class MemorySystem:
    def __init__(self):
        self.session_memory = {
            "conversation_history": [],
            "past_actions": [],
            "working_memory": "",
            "next_directive": "No current directive. System in initial starting state.",
            "journal": [],
            "plan": [],
            "current_objective": "",
            "commitments": [],
            "open_questions": [],
            "artifacts": [],
            "emotional_state": config.aria.initial_emotional_state.copy()
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
        """Store observation data with error handling"""
        try:
            self.session_memory["past_actions"].append({"step": step, "action": "observation"})
            self.session_memory["working_memory"] = observation.get("working_memory", "Error extracting working memory")
            self.session_memory["next_directive"] = observation.get("next_directive", "Continue with current objective")
            self.session_memory["plan"] = observation.get("plan", [])
            self.session_memory["current_objective"] = observation.get("current_objective", "No current objective defined")
            self.session_memory["emotional_state"] = observation.get("emotional_state", {})
            
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error storing observation: {e}")
            # Ensure we don't break the system
            self.session_memory["past_actions"].append({"step": step, "action": "observation_error"})
            self.session_memory["working_memory"] = f"Error storing observation: {str(e)}"

    def store_action(self, action, step):
        self.session_memory["past_actions"].append({"step": step, "action": action})

    def store_reflection(self, reflection):
        """Store reflection data with error handling"""
        try:
            self.session_memory["working_memory"] = reflection.get("updated_working_memory", "Error extracting updated working memory")
            self.session_memory["journal"].append(reflection.get("journal_entry", "Error extracting journal entry"))
            self.session_memory["next_directive"] = reflection.get("next_directive", "Continue with current objective")
            self.session_memory["plan"] = reflection.get("updated_plan", [])
            self.session_memory["emotional_state"] = reflection.get("emotional_state", {})
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error storing reflection: {e}")
            # Ensure we don't break the system
            self.session_memory["journal"].append(f"Error storing reflection: {str(e)}")