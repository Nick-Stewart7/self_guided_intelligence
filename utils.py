import boto3, json, random
from datetime import datetime

class ToolSystem:
    def __init__(self):
          self.s3_client = boto3.client('s3')
          self.bedrock_client = boto3.client(
               service_name="bedrock-agent"
          )
          self.agent_runtime_client = boto3.client(
               service_name="bedrock-agent-runtime"
          )
          self.bucket = "timekeepersmemory"

    def read_memory(self, query):
        response = self.agent_runtime_client.retrieve_and_generate(
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration":{
                    "modelArn": "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-2-90b-instruct-v1:0",
                    "knowledgeBaseId":"YKP6GR7DHT", 
                } 
            },
            input={"text": query}
        )
        print("Received response:" + json.dumps(response, ensure_ascii=False))
        response_output = response['output']['text']
        return response_output
    def write_memory(self, memory_type, memory_content):
        filename = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        memory_data = {
            "timestamp": datetime.now().isoformat(),
            "type": memory_type,
            "content": memory_content
        }
        print(f"Attempting to write to S3 bucket: {self.bucket}, file {filename}")
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=filename,
            Body=json.dumps(memory_data)
        )
        print("Ingesting file to knowledge base...")
        self.bedrock_client.start_ingestion_job(
            dataSourceId="CYK36FCQQX",
            knowledgeBaseId="YKP6GR7DHT"
        )
        print("Successful")
        return "written memory"
