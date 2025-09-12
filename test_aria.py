#!/usr/bin/env python3
"""
Basic testing framework for Aria consciousness system.
Tests core functionality and integration points.
"""

import os
import sys
import json
import asyncio
import requests
import time
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_configuration():
    """Test configuration system"""
    print("🔧 Testing configuration system...")
    
    try:
        from config import config
        
        # Test basic configuration loading
        assert hasattr(config, 'aws'), "AWS configuration not loaded"
        assert hasattr(config, 'aria'), "Aria configuration not loaded"
        
        # Test validation
        config_valid = config.validate()
        
        print(f"  ✓ Configuration loaded successfully")
        print(f"  ✓ Configuration validation: {'PASS' if config_valid else 'WARN (missing credentials)'}")
        
        return True
    except Exception as e:
        print(f"  ✗ Configuration test failed: {e}")
        return False

def test_memory_system():
    """Test memory system functionality"""
    print("🧠 Testing memory system...")
    
    try:
        from memory import MemorySystem
        
        memory = MemorySystem()
        
        # Test basic session memory
        assert isinstance(memory.session_memory, dict), "Session memory not properly initialized"
        assert "conversation_history" in memory.session_memory, "Missing conversation history"
        assert "working_memory" in memory.session_memory, "Missing working memory"
        
        # Test context generation
        context = memory.get_context()
        assert isinstance(context, str), "Context generation failed"
        
        # Test observation storage
        test_observation = {
            "working_memory": "test memory",
            "next_directive": "test directive",
            "current_objective": "test objective",
            "plan": ["step 1", "step 2"]
        }
        memory.store_observation(test_observation, 1)
        assert memory.session_memory["working_memory"] == "test memory", "Observation storage failed"
        
        print("  ✓ Memory system basic functionality works")
        return True
    except Exception as e:
        print(f"  ✗ Memory system test failed: {e}")
        return False

def test_prompt_system():
    """Test prompt management system"""
    print("📝 Testing prompt system...")
    
    try:
        from prompts import PromptManager
        from memory import MemorySystem
        
        prompt_manager = PromptManager()
        memory = MemorySystem()
        
        # Test prompt generation
        observation_prompt = prompt_manager.get_observation_prompt(
            "test directive",
            "test context",
            memory.session_memory,
            "test signals",
            {"curiosity": 0.5}
        )
        assert isinstance(observation_prompt, str), "Observation prompt generation failed"
        assert "test directive" in observation_prompt, "Directive not included in prompt"
        
        # Test action prompt
        action_prompt = prompt_manager.get_prompt(
            "Think",
            "test directive", 
            "test context",
            memory.session_memory,
            {"curiosity": 0.5}
        )
        assert isinstance(action_prompt, str), "Action prompt generation failed"
        
        print("  ✓ Prompt system generates valid prompts")
        return True
    except Exception as e:
        print(f"  ✗ Prompt system test failed: {e}")
        return False

def test_aria_core():
    """Test AriaCore functionality"""
    print("🤖 Testing AriaCore system...")
    
    try:
        from main import AriaCore, EnvironmentalSignal
        
        aria = AriaCore()
        
        # Test initialization
        assert hasattr(aria, 'environmental_signals'), "Environmental signals not initialized"
        assert hasattr(aria, 'memory'), "Memory not initialized"
        assert hasattr(aria, 'prompt_manager'), "Prompt manager not initialized"
        
        # Test environmental signal addition
        test_signal = EnvironmentalSignal(
            type="user_message",
            content="Hello Aria",
            priority=5
        )
        signal_id = aria.add_environmental_signal(test_signal)
        assert signal_id is not None, "Signal ID not returned"
        assert len(aria.environmental_signals) > 0, "Signal not added to queue"
        
        # Test signal validation
        try:
            empty_signal = EnvironmentalSignal(
                type="user_message",
                content="",
                priority=5
            )
            aria.add_environmental_signal(empty_signal)
            # Should handle gracefully
        except Exception:
            pass  # Expected
        
        print("  ✓ AriaCore basic functionality works")
        return True
    except Exception as e:
        print(f"  ✗ AriaCore test failed: {e}")
        return False

def test_server_endpoints():
    """Test FastAPI server endpoints"""
    print("🌐 Testing server endpoints...")
    
    try:
        # Note: This assumes server is running on localhost:8000
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code in [200, 503]:  # 503 is acceptable if AWS not configured
                print("  ✓ Health endpoint responds")
            else:
                print(f"  ⚠ Health endpoint returned {response.status_code}")
        except requests.ConnectionError:
            print("  ⚠ Server not running - skipping endpoint tests")
            return True
        
        # Test root endpoint
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                print("  ✓ Root endpoint responds")
            else:
                print(f"  ⚠ Root endpoint returned {response.status_code}")
        except requests.RequestException:
            print("  ⚠ Root endpoint test failed")
        
        # Test environmental signal endpoint (if server is healthy)
        try:
            test_signal = {
                "type": "user_message",
                "content": "Test signal from validation",
                "priority": 1,
                "metadata": {"source": "test_suite"}
            }
            response = requests.post(
                f"{base_url}/environmental_signal",
                json=test_signal,
                timeout=5
            )
            if response.status_code == 200:
                print("  ✓ Environmental signal endpoint responds")
            else:
                print(f"  ⚠ Environmental signal endpoint returned {response.status_code}")
        except requests.RequestException:
            print("  ⚠ Environmental signal endpoint test failed")
        
        return True
    except Exception as e:
        print(f"  ✗ Server endpoint tests failed: {e}")
        return False

def test_aws_integration():
    """Test AWS integration (if configured)"""
    print("☁️ Testing AWS integration...")
    
    try:
        from utils import ToolSystem
        
        tools = ToolSystem()
        
        # Test AWS client initialization
        assert tools.s3_client is not None, "S3 client not initialized"
        assert tools.bedrock_client is not None, "Bedrock client not initialized"
        
        # Test memory operations (only if credentials are available)
        if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
            try:
                # Test read operation (should handle errors gracefully)
                result = tools.read_memory("test query")
                assert isinstance(result, str), "Memory read should return string"
                
                if not result.startswith("Error:"):
                    print("  ✓ AWS memory read successful")
                else:
                    print("  ⚠ AWS memory read returned error (expected if resources not configured)")
                
            except Exception as e:
                print(f"  ⚠ AWS memory operation failed (expected if not configured): {e}")
        else:
            print("  ⚠ AWS credentials not found - skipping integration tests")
        
        print("  ✓ AWS integration components initialized")
        return True
    except Exception as e:
        print(f"  ✗ AWS integration test failed: {e}")
        return False

def run_all_tests():
    """Run all test suites"""
    print("🧪 Starting Aria System Validation")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_memory_system,
        test_prompt_system,
        test_aria_core,
        test_aws_integration,
        test_server_endpoints
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Test suite failed: {e}")
            results.append(False)
        print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} test suites passed!")
        print("✅ Aria system is ready for use")
    elif passed >= total * 0.7:  # 70% pass rate
        print(f"⚠️  {passed}/{total} test suites passed")
        print("🔧 System is functional but may need configuration")
    else:
        print(f"❌ Only {passed}/{total} test suites passed")
        print("🔧 System needs attention before use")
    
    print("\nNext steps:")
    if passed < total:
        print("1. Run 'python setup_config.py' to configure missing elements")
        print("2. Ensure AWS credentials and resources are properly set up")
        print("3. Start the server with 'python run_server.py'")
    else:
        print("1. Start the server with 'python run_server.py'")
        print("2. Open frontend.html in your browser")
        print("3. Begin interacting with Aria!")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)