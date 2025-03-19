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
            "next_action": "",
            "short_term_memory": {
                "active_context": "",
                "next_directive": ""
            },
            "long_term_memory": {
                "key_insights": [],
                "unresolved_paths": []
            }  
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

    def save_to_long_term(self, data):
        """Writes memory to persistent storage (AWS API)."""
        self.long_term_memory_api.put_object(
            Bucket="your-memory-bucket",
            Key="memory_log.json",
            Body=json.dumps(data)
        )

    def retrieve_memory(self, query):
        """Retrieves relevant memories from long-term storage using RAG."""
        return f"[RAG Search Results for {query}]"
