from typing import Dict, Optional, Any
from pydantic import BaseModel
import asyncio
import json
import time
import boto3
from datetime import datetime
from collections import deque
import uuid
from memory import MemorySystem
from prompts import PromptManager
from utils import ToolSystem
from config import config

# Pydantic models for API contracts
class EnvironmentalSignal(BaseModel):
    type: str  # "user_message", "system_event", "external_data", etc.
    content: Any
    priority: int = 1  # 1-10, higher = more urgent
    metadata: Dict[str, Any] = {}

class MindState(BaseModel):
    current_focus: Optional[str]
    working_memory: str
    environmental_signals_pending: int
    emotional_state: Dict[str, float]

class AriaCore:
    def __init__(self):
        self.environmental_signals = deque(maxlen=config.aria.max_environmental_signals)
        self.running = False
        self.mind_state_subscribers = set()
        self.memory = MemorySystem()
        self.prompt_manager = PromptManager()
        self.tools = ToolSystem()
        self.step = 0
        self.context = self.memory.get_context()

    def observe(self, aggregate):
        """
        Observe phase - Aria notices her internal state and environment then she decides her next action.
        """
        try:
            observation_prompt = self.prompt_manager.get_observation_prompt(
                self.context,
                self.memory.session_memory,
                aggregate
            )

            # Debug log
            print(f"\033[1;31m{observation_prompt}")
            
            # Call LLM to get observation
            observation = self.call_llm(observation_prompt)
            
            # Check for error responses
            if observation.startswith("Error:"):
                print(f"LLM error in observation: {observation}")
                # Return a fallback observation
                #Todo create a useful fallback observation
                return {
                    "working_memory": "Error in observation processing",
                    "thoughts": "Experiencing technical difficulties",
                    "signal_analysis": "Unable to process signals",
                    "current_objective": "Recovery from error state",
                    "plan": ["Attempt to recover from error", "Continue with minimal functionality"],
                    "next_action": "Think",
                    "next_directive": "Focus on basic functionality while recovering",
                    "explanation": "System is in error recovery mode",
                    "self_narration": "Encountered technical difficulties, attempting recovery",
                    "emotional_state": {"uncertainty": 1.0, "determination": 1.0}
                }
            
            # Format for reading
            try:
                parsed_observation = json.loads(observation.strip())
            except json.JSONDecodeError as e:
                print(f"JSON parsing error in observation: {e}")
                print(f"Raw observation: {observation}")
                # Return fallback observation
                #Todo create a useful fallback observation
                return {
                    "working_memory": "JSON parsing error in observation",
                    "thoughts": "Unable to parse observation response",
                    "signal_analysis": "Response format error",
                    "current_objective": "Parse and process observations correctly",
                    "plan": ["Fix response formatting", "Continue with processing"],
                    "next_action": "Think",
                    "next_directive": "Focus on generating properly formatted responses",
                    "explanation": "Response parsing failed, using fallback",
                    "self_narration": "Encountered formatting error, using fallback response",
                    "emotional_state": {"confusion": 0.7, "focus": 0.5}
                }

            # Store in memory so Aria "remembers" her past evaluations
            self.memory.store_observation(parsed_observation)

            return parsed_observation
            
        except Exception as e:
            print(f"Critical error in observe method: {e}")
            # Return emergency fallback
            return {
                "working_memory": "Critical system error",
                "thoughts": "Emergency recovery mode activated",
                "signal_analysis": "System error detected",
                "current_objective": "Recover from critical error",
                "plan": ["Emergency recovery", "Basic functionality restoration"],
                "next_action": "Think",
                "next_directive": "Emergency recovery procedures",
                "explanation": "Critical error occurred, emergency recovery",
                "self_narration": "System entered emergency recovery mode",
                "emotional_state": {"alarm": 0.9, "resilience": 0.4}
            }

    def execute_action(self, observation):
        """
        Action phase - Aria executes based on her observation.
        """
        plan = self.memory.session_memory["plan"]
        print(f"Current plan: {plan}")
        batch = ""
        for step in plan:
            directive = step.get("description", "No directive provided")
            parameters = step.get("parameters", [])
            output = "No output generated"
            if "status" not in step:
                step["status"] = "pending"
            if step["status"] == "completed":
                continue  # Skip already completed steps
            # Execute the action
            #todo create unique action execution system
            action = step["action"]
            match action:
                case "Think":
                    prompt = self.prompt_manager.get_action_prompt(
                        self.context,
                        self.memory.session_memory,
                        action,
                        directive
                    )
                    output = self.call_llm(prompt)
                case "Plan":
                    prompt = self.prompt_manager.get_action_prompt(
                        self.context,
                        self.memory.session_memory,
                        action,
                        directive
                    )
                    output = self.call_llm(prompt)
                case "Read":
                    file_path = observation.get("file_path", "unknown.txt")
                    output = self.tools.read_file(file_path)
                case "Write":
                    file_path = parameters[0] if parameters else "unknown.txt"
                    content = parameters[1] if len(parameters) > 1 else "No content provided"
                    output = self.tools.write_file(file_path, content)
                case "Edit":
                    #Todo write edit logic - read file the re-write with changes using LLM
                    file_path = observation.get("file_path", "unknown.txt")
                    content = self.tools.read_file(file_path)
                    output =  self.tools.write_file(file_path, content)
                case "Code":
                    #Todo write code logic - create custom prompt for coding tasks
                    prompt = self.prompt_manager.get_action_prompt(
                        self.context,
                        self.memory.session_memory,
                        action,
                        directive
                    )
                    output = self.call_llm(prompt)
                case "Recall":
                    query = observation.get("query", "")
                    output = self.tools.read_memory(query)
                case "Memorize":
                    #memory_type = observation.get("memory_type", "general")
                    memory_content = observation.get("memory_content", "")
                    output = self.tools.write_memory(memory_content)
                case "Search":
                    query = parameters[0] if parameters else "latest news"
                    output = self.tools.web_search(query)
                case "Respond":
                    prompt = self.prompt_manager.get_action_prompt(
                        self.context,
                        self.memory.session_memory,
                        action,
                        directive
                    )
                    output = self.call_llm(prompt)
                    # Emit event to notifiy any listeners (e.g., UI) of new response
                    # Mark user input as responded to in memory
                case "Wander":
                    prompt = self.prompt_manager.get_action_prompt(
                        self.context,
                        self.memory.session_memory,
                        action,
                        directive
                    )
                    output = self.call_llm(prompt)
            
            self.memory.store_action(action, self.step, output)
            if step["status"] != "completed":
                step["status"] = "completed"
                time.sleep(5)  # Simulate time taken to perform action
            batch += f"Action: {action}\nOutput: {output}\n\n"
        self.step += 1
        return batch


    def reflect(self, response):
        """
        Reflection phase - Aria integrates insights and updates her understanding.
        """
        try:
            reflection_prompt = self.prompt_manager.get_reflection_prompt(
                self.context,
                self.memory.session_memory,
                response
            )
            print(f"\033[1;31m{reflection_prompt}")

            reflection_output = self.call_llm(reflection_prompt)
            
            # Check for error responses
            if reflection_output.startswith("Error:"):
                print(f"LLM error in reflection: {reflection_output}")
                # Create fallback reflection
                fallback_reflection = {
                    "updated_working_memory": "Error in reflection processing",
                    "thoughts": "Unable to process reflection due to technical difficulties",
                    "meta_analysis": "Reflection processing failed, maintaining current state",
                    "journal_entry": "System error during reflection phase",
                    "updated_plan": ["Continue with current plan", "Monitor for system stability"],
                    "next_directive": "Continue with previous directive while monitoring system health"
                }
                self.memory.store_reflection(fallback_reflection)
                return json.dumps(fallback_reflection)
            
            try:
                reflection = json.loads(reflection_output.strip())
            except json.JSONDecodeError as e:
                print(f"JSON parsing error in reflection: {e}")
                print(f"Raw reflection: {reflection_output}")
                # Create fallback reflection
                fallback_reflection = {
                    "updated_working_memory": "JSON parsing error in reflection",
                    "thoughts": "Unable to parse reflection response properly",
                    "meta_analysis": "Response formatting issue detected",
                    "journal_entry": "Encountered formatting error during reflection",
                    "updated_plan": ["Fix response formatting", "Continue processing"],
                    "next_directive": "Focus on generating properly formatted responses"
                }
                self.memory.store_reflection(fallback_reflection)
                return json.dumps(fallback_reflection)

            self.memory.store_reflection(reflection)
            return reflection_output
            
        except Exception as e:
            print(f"Critical error in reflect method: {e}")
            # Emergency fallback reflection
            emergency_reflection = {
                "updated_working_memory": "Critical error during reflection",
                "thoughts": "Emergency recovery mode in reflection phase",
                "meta_analysis": "System encountered critical error",
                "journal_entry": "Emergency recovery activated during reflection",
                "updated_plan": ["Emergency recovery", "System stability check"],
                "next_directive": "Emergency recovery procedures"
            }
            self.memory.store_reflection(emergency_reflection)
            return json.dumps(emergency_reflection)

    def call_llm(self, prompt, size_flag=False, retries=3):
        """Handles API call to LLaMA3 with error handling and retries."""
        
        for attempt in range(retries):
            try:
                bedrock_client = boto3.client("bedrock-runtime")
                if size_flag:
                    model_id = config.aws.memory_model
                else:
                    model_id = config.aws.reasoning_model
                print("invoking model:", model_id)
                llm_params = config.get_llm_params()
                llm_response = bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "prompt": prompt,
                        **llm_params
                    })
                )
                return json.loads(llm_response.get('body').read())['generation']
                
            except Exception as e:
                print(f"LLM call attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    # Last attempt failed, return a fallback response
                    print("All LLM call attempts failed. Using fallback response.")
                    return f"Error: Unable to process request after {retries} attempts. Last error: {str(e)}"
                
                # Wait before retry (exponential backoff)
                time.sleep(2 ** attempt)
        
        return "Error: Unexpected failure in LLM call"

    def add_environmental_signal(self, signal: EnvironmentalSignal):
        """Add signal to Aria's environment - she'll notice when she's ready"""
        try:
            # Validate signal content
            if not signal.content or (isinstance(signal.content, str) and len(signal.content.strip()) == 0):
                raise ValueError("Signal content cannot be empty")
            
            if signal.priority < 1 or signal.priority > 10:
                raise ValueError("Signal priority must be between 1 and 10")
            
            # Validate signal type
            valid_types = ["user_message", "system_event", "external_data", "thought_prompt"]
            if signal.type not in valid_types:
                print(f"Warning: Unknown signal type '{signal.type}'. Using 'system_event' as fallback.")
                signal.type = "system_event"
            
            signal_with_id = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                **signal.dict()
            }
            self.environmental_signals.append(signal_with_id)
            self.last_updated = datetime.now()
            print(f"Added environmental signal: {signal.type} (priority: {signal.priority})")
            return signal_with_id["id"]
            
        except Exception as e:
            print(f"Error adding environmental signal: {e}")
            # Create a safe fallback signal
            fallback_signal = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "type": "system_event",
                "content": f"Error processing signal: {str(e)}",
                "priority": 1,
                "metadata": {"error": True, "original_signal": str(signal)}
            }
            self.environmental_signals.append(fallback_signal)
            self.last_updated = datetime.now()
            return fallback_signal["id"]
    
    def aggregate_signals(self):
        """Aggregate and prioritize signals"""
        if not self.environmental_signals:
            return None
        # Simple prioritization: highest priority first, then FIFO
        sorted_signals = sorted(self.environmental_signals, key=lambda s: (-s["priority"], s["timestamp"]))
        # Remove processed signals from the queue
        # Aggregate signals into a parsed format ready to be sent to the LLM
        prompt_insert = str(sorted_signals)  # Convert to string for LLM input
        # This could be a JSON object that feels like a document
        # For example, user input: "What's the weather like?"
        # System event: "New data available from sensor X"  
        # Current time: "2023-10-01T12:00:00Z"
        return prompt_insert
    
    def get_mind_state(self) -> MindState:
        """Current snapshot of Aria's mind"""
        print(f"Getting mind state at {datetime.now()}")
        print(f"Current directive: {self.memory.session_memory['next_directive']} | Pending signals: {len(self.environmental_signals)} | Emotional state: {self.memory.session_memory.get("emotional_state", {})} | Working memory: {self.memory.session_memory.get("working_memory", "No working memory")}")
        return MindState(
            current_focus=self.memory.session_memory.get("next_directive", "No current directive"),
            working_memory=self.memory.session_memory.get("working_memory", "No working memory"),
            environmental_signals_pending=len(self.environmental_signals),
            emotional_state=self.memory.session_memory.get("emotional_state", {})
        )

    async def natural_pause(self):
        """Aria's natural rhythm - not every thought is instant"""
        await asyncio.sleep(config.aria.natural_pause_seconds)

    async def mind_loop(self):
        """Aria's continuous consciousness with comprehensive error handling"""
        self.running = True
        cycle_count = 0
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while self.running:
            try:
                #await self.natural_pause()
                cycle_count += 1
                print(f"\033[1;35m--- Mind Cycle {cycle_count} ---\n")
                # Aggregate Signals with error handling
                try:
                    aggregate = self.aggregate_signals()
                except Exception as e:
                    print(f"Error aggregating signals: {e}")
                    aggregate = "Error: Unable to aggregate environmental signals"
                
                # Observe
                observation = self.observe(aggregate)
                print(f"\033[1;36mObservation:\n{observation}\n")
                await self.natural_pause()
                
                # Response
                response = self.execute_action(observation)
                print(f"\033[1;34mResponse:\n{response}\n")
                await self.natural_pause()
                
                # Reflect
                reflection = self.reflect(response)
                print(f"\033[1;32mReflection:\n{reflection}\n")
                await self.natural_pause()
                
                # Reset error counter on successful cycle
                consecutive_errors = 0
                    
            except Exception as e:
                consecutive_errors += 1
                print(f"Error in mind loop cycle {cycle_count}: {e}")
                print(f"Consecutive errors: {consecutive_errors}/{max_consecutive_errors}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print("Too many consecutive errors. Stopping mind loop for safety.")
                    self.running = False
                    break
                
                # Progressive recovery delays
                recovery_delay = min(30, 5 * consecutive_errors)
                print(f"Entering recovery mode for {recovery_delay} seconds...")
                await asyncio.sleep(recovery_delay)
    
    def stop_mind(self):
        """Gracefully stop Aria's mind loop"""
        self.running = False
        print("Stopping Aria's mind")
