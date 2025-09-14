"""
Configuration management for Aria consciousness system.
Handles environment variables, AWS resources, and system parameters.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class AWSConfig:
    """AWS-specific configuration"""
    region: str = "us-east-1"
    s3_bucket: str = ""
    knowledge_base_id: str = ""
    data_source_id: str = ""

    # Model ARNs - configurable per deployment
    reasoning_model: str = ""
    memory_model: str = ""


@dataclass
class AriaConfig:
    """Aria consciousness system configuration"""
    # Timing and behavior
    natural_pause_seconds: int = 30
    mind_loop_enabled: bool = True
    max_environmental_signals: int = 100

    # LLM parameters
    temperature: float = 0.5
    top_p: float = 0.9
    max_gen_len: int = 2048

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "info"

    # Initial emotional state
    initial_emotional_state: Dict[str, float] = {"curiosity": 0.5, "focus": 0.7}


class ConfigManager:
    """Centralized configuration management"""
    def __init__(self, config_file: Optional[str] = "config.template.json"):
        self.config_file = config_file
        self.aws = AWSConfig()
        self.aria = AriaConfig()   
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
config = ConfigManager("config.json")
