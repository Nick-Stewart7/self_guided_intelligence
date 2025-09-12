#!/usr/bin/env python3
"""
Configuration setup script for Aria consciousness system.
Helps users set up their environment and configuration files.
"""

import os
import sys
import json
from pathlib import Path

def create_env_file():
    """Create a .env file from template if it doesn't exist"""
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if env_file.exists():
        print(f"✓ .env file already exists at {env_file.absolute()}")
        return
    
    if template_file.exists():
        # Copy template to .env
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(template_content)
        
        print(f"✓ Created .env file from template at {env_file.absolute()}")
        print("  Please edit this file and add your AWS credentials and resource IDs")
    else:
        print("✗ Template file .env.template not found")

def create_config_template():
    """Create a configuration template file"""
    from config import ConfigManager
    
    config_manager = ConfigManager()
    config_manager.save_template("config.template.json")
    print("✓ Created config.template.json")

def check_aws_credentials():
    """Check if AWS credentials are available"""
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if aws_access_key and aws_secret_key:
        print("✓ AWS credentials found in environment")
        return True
    else:
        print("✗ AWS credentials not found in environment")
        print("  Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return False

def check_required_aws_resources():
    """Check if required AWS resource IDs are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    resources = {
        "S3 Bucket": os.getenv("ARIA_S3_BUCKET", "timekeepersmemory"),
        "Knowledge Base ID": os.getenv("ARIA_KNOWLEDGE_BASE_ID", "YKP6GR7DHT"),
        "Data Source ID": os.getenv("ARIA_DATA_SOURCE_ID", "CYK36FCQQX")
    }
    
    default_values = ["timekeepersmemory", "YKP6GR7DHT", "CYK36FCQQX"]
    
    print("\nAWS Resource Configuration:")
    all_configured = True
    
    for name, value in resources.items():
        if value in default_values:
            print(f"  ⚠️  {name}: {value} (using default - please configure)")
            all_configured = False
        else:
            print(f"  ✓ {name}: {value}")
    
    return all_configured

def test_configuration():
    """Test if the configuration is working"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        from config import config
        
        print("\nTesting configuration...")
        
        if config.validate():
            print("✓ Configuration validation passed")
            return True
        else:
            print("✗ Configuration validation failed")
            return False
            
    except Exception as e:
        print(f"✗ Error testing configuration: {e}")
        return False

def main():
    """Main setup process"""
    print("Aria Consciousness System - Configuration Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    print("\n1. Setting up environment file...")
    create_env_file()
    
    # Step 2: Create config template
    print("\n2. Creating configuration template...")
    create_config_template()
    
    # Step 3: Check AWS credentials
    print("\n3. Checking AWS credentials...")
    aws_creds_ok = check_aws_credentials()
    
    # Step 4: Check AWS resources
    print("\n4. Checking AWS resource configuration...")
    aws_resources_ok = check_required_aws_resources()
    
    # Step 5: Test configuration
    print("\n5. Testing configuration...")
    config_ok = test_configuration()
    
    # Summary
    print("\n" + "=" * 50)
    print("SETUP SUMMARY")
    print("=" * 50)
    
    if aws_creds_ok and config_ok:
        print("✓ Setup complete! You can now run: python run_server.py")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
        
        if not aws_creds_ok:
            print("\nNext steps:")
            print("1. Add your AWS credentials to the .env file:")
            print("   AWS_ACCESS_KEY_ID=your_access_key")
            print("   AWS_SECRET_ACCESS_KEY=your_secret_key")
        
        if not aws_resources_ok:
            print("2. Configure your AWS resource IDs in the .env file:")
            print("   ARIA_S3_BUCKET=your-s3-bucket-name")
            print("   ARIA_KNOWLEDGE_BASE_ID=your-knowledge-base-id")
            print("   ARIA_DATA_SOURCE_ID=your-data-source-id")
    
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()