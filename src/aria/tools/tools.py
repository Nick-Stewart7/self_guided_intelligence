import uuid
from self_guided_ai.config.config import config
import chromadb
from tavily import TavilyClient


class ToolSystem:
    def __init__(self):
          self.config = config
          self.chroma_client = chromadb.Client()
          self.collection = self.chroma_client.create_collection(name="long_term_memory")

    def write_memory(self, memory):
        """Write memory to long-term storage with error handling"""
        try:
            memory_id = str(uuid.uuid4())
            self.collection.add(
                ids=[memory_id],
                documents=[memory]
            )
        except Exception as e:
            print(f"Error writing memory: {e}")
        return "Memory written successfully"
    
    def read_memory(self, query, n_results=5):
        """Read memory from long-term storage with error handling"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print(f"Error reading memory: {e}")
            return []

    def read_file(self, file_path):
        """Read a file with error handling"""
        try:
            f = open(file_path, 'r', encoding='utf-8')
            content = f.read()
            f.close()   
            return content
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return f"Error: Unable to read file {file_path}. {str(e)}"
        
    def write_file(self, file_path, content):
        """Write a file with error handling"""
        try:
            f = open(file_path, 'w', encoding='utf-8')
            f.write(content)
            f.close()
            return "File written successfully"
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return f"Error: Unable to write file {file_path}. {str(e)}"
    
    def web_search(self, query):
        print(self.config.tavily.api_key)
        tavily_client = TavilyClient(api_key=self.config.tavily.api_key)
        try:
            results = tavily_client.search(query)
            return results
        except Exception as e:
            print(f"Error performing web search: {e}")
            return [f"Error: Unable to perform web search. {str(e)}"]