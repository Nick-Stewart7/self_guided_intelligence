import boto3, json, random
from datetime import datetime
from config import config

class ToolSystem:
    def __init__(self):
          self.s3_client = boto3.client('s3', region_name=config.aws.region)
          self.bedrock_client = boto3.client(
               service_name="bedrock-agent",
               region_name=config.aws.region
          )
          self.agent_runtime_client = boto3.client(
               service_name="bedrock-agent-runtime",
               region_name=config.aws.region
          )
          self.bucket = config.aws.s3_bucket

    def read_memory(self, query, retries=3):
        """Read from long-term memory with error handling and retries"""
        for attempt in range(retries):
            try:
                if not query or len(query.strip()) == 0:
                    return "Error: Empty query provided for memory read"
                
                response = self.agent_runtime_client.retrieve_and_generate(
                    retrieveAndGenerateConfiguration={
                        "type": "KNOWLEDGE_BASE",
                        "knowledgeBaseConfiguration":{
                            "modelArn": config.aws.memory_model,
                            "knowledgeBaseId": config.aws.knowledge_base_id, 
                        } 
                    },
                    input={"text": query}
                )
                print("Received response:" + json.dumps(response, ensure_ascii=False))
                
                if 'output' in response and 'text' in response['output']:
                    return response['output']['text']
                else:
                    print(f"Unexpected response format: {response}")
                    return "Error: Unexpected response format from memory system"
                    
            except Exception as e:
                print(f"Memory read attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    return f"Error: Unable to read memory after {retries} attempts. Last error: {str(e)}"
                
                # Wait before retry
                import time
                time.sleep(2 ** attempt)
        
        return "Error: Unexpected failure in memory read"
    def write_memory(self, memory_type, memory_content, retries=3):
        """Write to long-term memory with error handling and retries"""
        for attempt in range(retries):
            try:
                if not memory_content or (isinstance(memory_content, str) and len(memory_content.strip()) == 0):
                    return "Error: Empty memory content provided"
                
                if not memory_type or len(memory_type.strip()) == 0:
                    memory_type = "general"
                
                filename = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}.json"
                memory_data = {
                    "timestamp": datetime.now().isoformat(),
                    "type": memory_type,
                    "content": memory_content
                }
                
                print(f"Attempting to write to S3 bucket: {self.bucket}, file {filename}")
                self.s3_client.put_object(
                    Bucket=self.bucket,
                    Key=filename,
                    Body=json.dumps(memory_data, ensure_ascii=False, indent=2)
                )
                
                # Try to start ingestion job (non-critical)
                try:
                    print("Ingesting file to knowledge base...")
                    self.bedrock_client.start_ingestion_job(
                        dataSourceId=config.aws.data_source_id,
                        knowledgeBaseId=config.aws.knowledge_base_id
                    )
                    print("Ingestion job started successfully")
                except Exception as ingestion_error:
                    print(f"Warning: Ingestion job failed but memory was saved: {ingestion_error}")
                
                return "Memory written successfully"
                
            except Exception as e:
                print(f"Memory write attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    return f"Error: Unable to write memory after {retries} attempts. Last error: {str(e)}"
                
                # Wait before retry
                import time
                time.sleep(2 ** attempt)
        
        return "Error: Unexpected failure in memory write"
