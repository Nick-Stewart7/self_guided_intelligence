"""
Configuration management for Aria consciousness system.
Handles environment variables, AWS resources, and system parameters.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class AWSConfig:
    """AWS-specific configuration"""
    region: str = "us-east-1"
    s3_bucket: str = "timekeepersmemory"
    knowledge_base_id: str = "YKP6GR7DHT"
    data_source_id: str = "CYK36FCQQX"
    
    # Model ARNs - configurable per deployment
    reasoning_model: str = "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-3-70b-instruct-v1:0"
    memory_model: str = "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-2-90b-instruct-v1:0"


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
    initial_emotional_state: Dict[str, float] = None
    
    def __post_init__(self):
        if self.initial_emotional_state is None:
            self.initial_emotional_state = {"curiosity": 0.5, "focus": 0.7}


class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.aws = AWSConfig()
        self.aria = AriaConfig()
        
        # Load from environment variables
        self._load_from_env()
        
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # AWS Configuration
        self.aws.region = os.getenv("ARIA_AWS_REGION", self.aws.region)
        self.aws.s3_bucket = os.getenv("ARIA_S3_BUCKET", self.aws.s3_bucket)
        self.aws.knowledge_base_id = os.getenv("ARIA_KNOWLEDGE_BASE_ID", self.aws.knowledge_base_id)
        self.aws.data_source_id = os.getenv("ARIA_DATA_SOURCE_ID", self.aws.data_source_id)
        self.aws.reasoning_model = os.getenv("ARIA_REASONING_MODEL", self.aws.reasoning_model)
        self.aws.memory_model = os.getenv("ARIA_MEMORY_MODEL", self.aws.memory_model)
        
        # Aria Configuration
        self.aria.natural_pause_seconds = int(os.getenv("ARIA_PAUSE_SECONDS", self.aria.natural_pause_seconds))
        self.aria.mind_loop_enabled = os.getenv("ARIA_MIND_LOOP_ENABLED", "true").lower() == "true"
        self.aria.max_environmental_signals = int(os.getenv("ARIA_MAX_SIGNALS", self.aria.max_environmental_signals))
        
        # LLM Parameters
        self.aria.temperature = float(os.getenv("ARIA_TEMPERATURE", self.aria.temperature))
        self.aria.top_p = float(os.getenv("ARIA_TOP_P", self.aria.top_p))
        self.aria.max_gen_len = int(os.getenv("ARIA_MAX_GEN_LEN", self.aria.max_gen_len))
        
        # Server Configuration
        self.aria.host = os.getenv("ARIA_HOST", self.aria.host)
        self.aria.port = int(os.getenv("ARIA_PORT", self.aria.port))
        self.aria.reload = os.getenv("ARIA_RELOAD", "true").lower() == "true"
        self.aria.log_level = os.getenv("ARIA_LOG_LEVEL", self.aria.log_level)
    
    def _load_from_file(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
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
                        
        except Exception as e:
            print(f"Warning: Failed to load config file {config_file}: {e}")
    
    def save_template(self, output_file: str = "config.template.json"):
        """Save a template configuration file"""
        template = {
            "aws": {
                "region": self.aws.region,
                "s3_bucket": "your-s3-bucket-name",
                "knowledge_base_id": "your-knowledge-base-id",
                "data_source_id": "your-data-source-id",
                "reasoning_model": "your-reasoning-model-arn",
                "memory_model": "your-memory-model-arn"
            },
            "aria": {
                "natural_pause_seconds": self.aria.natural_pause_seconds,
                "mind_loop_enabled": self.aria.mind_loop_enabled,
                "max_environmental_signals": self.aria.max_environmental_signals,
                "temperature": self.aria.temperature,
                "top_p": self.aria.top_p,
                "max_gen_len": self.aria.max_gen_len,
                "host": self.aria.host,
                "port": self.aria.port,
                "reload": self.aria.reload,
                "log_level": self.aria.log_level,
                "initial_emotional_state": self.aria.initial_emotional_state
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"Configuration template saved to {output_file}")
    
    def validate(self) -> bool:
        """Validate that required configuration is present"""
        required_env_vars = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY"
        ]
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"Missing required environment variables: {missing_vars}")
            return False
        
        # Validate AWS resource IDs are not default values
        if self.aws.knowledge_base_id == "YKP6GR7DHT":
            print("Warning: Using default knowledge base ID. Please configure ARIA_KNOWLEDGE_BASE_ID")
        
        if self.aws.s3_bucket == "timekeepersmemory":
            print("Warning: Using default S3 bucket. Please configure ARIA_S3_BUCKET")
        
        return True
    
    def get_llm_params(self) -> Dict[str, Any]:
        """Get LLM parameters for API calls"""
        return {
            "temperature": self.aria.temperature,
            "top_p": self.aria.top_p,
            "max_gen_len": self.aria.max_gen_len
        }


# Global configuration instance
config = ConfigManager()