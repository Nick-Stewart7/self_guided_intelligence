"""
Configuration management for Aria consciousness system.
Handles environment variables, AWS resources, and system parameters.
"""
from typing import Dict, Any, Optional
import json


class AWSConfig:
    def __init__(self):
        self.region = "us-west-2"
        self.s3_bucket = ""  # Default S3 bucket for long-term memory
        self.knowledge_base_id = ""  # Default knowledge base ID
        self.data_source_id = ""  # Default data source ID
        self.reasoning_model = ""  # Default reasoning model ARN
        self.memory_model = ""  # Default memory model ARN


class AriaConfig:
    def __init__(self):
        # Timing and behavior
        self.natural_pause_seconds = 30
        self.mind_loop_enabled = True
        self.max_environmental_signals = 100

        # LLM parameters
        self.temperature = 0.5
        self.top_p = 0.9
        self.max_gen_len = 2048

        # Server configuration
        self.host = "0.0.0.0"
        self.port = 8000
        self.reload = True
        self.log_level = "info"

        # Initial emotional state
        self.initial_emotional_state = {"curiosity": 0.5, "focus": 0.7}

class TavilyConfig:
    def __init__(self):
        self.api_key = ""  # Default Tavily API key

class ConfigManager:
    """Centralized configuration management"""
    def __init__(self, config_file: Optional[str] = "config.template.json"):
        self.config_file = config_file
        self.aws = AWSConfig()
        self.aria = AriaConfig()  
        self.tavily =  TavilyConfig()
        # Load from config file if provided
        self._load_from_file(config_file)

        self._validate()

    def _load_from_file(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)      
            # Update AWS config
            if 'aws' in config_data:
                aws_config = config_data['aws']
                for key, value in aws_config.items():
                    if hasattr(self.aws, key):
                        setattr(self.aws, key, value)        
            # Update Aria config
            if 'aria' in config_data:
                aria_config = config_data['aria']
                for key, value in aria_config.items():
                    if hasattr(self.aria, key):
                        setattr(self.aria, key, value)       
            # Update Tavily config
            if 'tavily' in config_data:
                tavily_config = config_data['tavily']
                for key, value in tavily_config.items():
                    if hasattr(self.tavily, key):
                        setattr(self.tavily, key, value)            
        except (TypeError, ValueError, AttributeError) as e:
            print(f"Warning: Failed to load config file {config_file}: {e}")
    def _validate(self) -> bool:
        """Validate that required configuration is present"""
        # Validate AWS resource IDs are not default values
        if self.aws.knowledge_base_id == "":
            print("Warning: Missing default knowledge base ID. Please configure ARIA_KNOWLEDGE_BASE_ID")
        if self.aws.s3_bucket == "":
            print("Warning: Missing default S3 bucket. Please configure ARIA_S3_BUCKET")
        if self.aws.data_source_id == "":
            print("Warning: Missing default data source ID. Please configure ARIA_DATA_SOURCE_ID")
        if self.aws.reasoning_model == "":
            print("Warning: Missing default reasoning model ARN. Please configure ARIA_REASONING_MODEL")
        if self.aws.memory_model == "":
            print("Warning: Missing default memory model ARN. Please configure ARIA_MEMORY_MODEL")

    def get_llm_params(self) -> Dict[str, Any]:
        """Get LLM parameters for API calls"""
        return {
            "temperature": self.aria.temperature,
            "top_p": self.aria.top_p,
            "max_gen_len": self.aria.max_gen_len
        }

# Global configuration instance
config = ConfigManager("./config/config.json")
