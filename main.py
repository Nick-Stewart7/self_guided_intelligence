from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
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

# Pydantic models for API contracts
class EnvironmentalSignal(BaseModel):
    type: str  # "user_message", "system_event", "external_data", etc.
    content: Any
    priority: int = 1  # 1-10, higher = more urgent
    metadata: Dict[str, Any] = {}

class MindState(BaseModel):
    current_focus: Optional[str]
    working_memory: Dict[str, Any]
    recent_thoughts: List[str]
    environmental_signals_pending: int
    last_updated: datetime
    emotional_state: Dict[str, float] = {}

class AriaCore:
    def __init__(self):
        self.environmental_signals = deque()
        self.current_focus = None
        self.recent_thoughts = deque(maxlen=10)  # Keep last 10 thoughts
        self.emotional_state = {"curiosity": 0.5, "focus": 0.7}
        self.running = False
        self.mind_state_subscribers = set()
        self.last_updated = datetime.now()
        self.memory = MemorySystem()
        self.prompt_manager = PromptManager()
        self.tools = ToolSystem()
        self.step = 0
        self.context = self.memory.get_context()
        self.thoughts = []

    def observe(self, current_directive, aggregate, current_focus, emotional_state):
        """
        Determines if the input requires reasoning 
        or 
        a simple answer and provides meta-cognitive oversight.
        """

        print(f"Observe Context:\n\033[0;37m{self.context}\n======\n{aggregate}\n======\nFocus:\n{current_focus}\n======\nEmotional State:\n{emotional_state}\n======\n")

        observation_prompt = self.prompt_manager.get_observation_prompt(
            current_directive,
            self.context,
            self.memory.session_memory,
            aggregate,
            emotional_state,
            current_focus
        )
        print(f"\033[1;31m{observation_prompt}")

        observation = self.call_llm(observation_prompt)
        print(f"\033[0;36mMeta-Observation:\n{observation}\n")
        self.thoughts.append(observation)

        # Format for reading
        parsed_observation = json.loads(observation.strip())

        # Store in memory so Aria "remembers" her past evaluations
        self.memory.store_observation(parsed_observation, self.step)

        self.step += 1

        return parsed_observation

    def execute_action(self, observation):
        '''
        Open-Ended Creativity Sparks

        Introspective Audits

        Knowledge Integration Sweeps

        Thought Refinement

        Dreaming Mode (wild speculative exploration)
        '''
        ### 🧠 AI DECIDES WHAT TO DO NEXT:
        decision = observation["next_action"]
        print(f"\033[1;32m{decision}")
        #parameters = observation["parameters"]
        response = ""

        response = self.run_action(self.memory.session_memory["next_directive"], decision)
        return response

    def run_action(self, directive, action):
        print(f"REASONING CONTEXT:\n\033[0;37m{self.context}\n======\n")

        prompt = self.prompt_manager.get_prompt(
            action,
            directive,
            self.context,
            self.memory.session_memory
        )
        print(f"\033[1;31m{prompt}")

        output = self.call_llm(prompt)
        print(f"\033[1;30mReasoning:\n{output}\n")
        self.thoughts.append(output)
        self.memory.store_action(action, self.step)

        self.step += 1
        return output

    def reflect(self, observation, response):

        reflection_prompt = self.prompt_manager.get_reflection_prompt(
            response,
            observation,
            self.context,
            self.memory.session_memory
        )
        print(f"\033[1;37m{reflection_prompt}")

        reflection_output = self.call_llm(reflection_prompt)

        reflection = json.loads(reflection_output.strip())

        self.memory.store_reflection(reflection)

        return reflection_output

    def run_read_memory(self, query):
        query_response = self.tools.read_memory(query)

        self.memory.session_memory["past_actions"].append(
            {
                "step": self.step,
                "action": "Retrieve Memory"
            }
        )
        self.step += 1

        return query_response

    def run_write_memory(self, memory_type, memory_content):
        success = self.tools.write_memory(memory_type, memory_content)

        self.memory.session_memory["past_actions"].append(
            {
                "step": self.step,
                "action": "Write Memory"
            }
        )
        self.step += 1

        return success

    def call_llm(self, prompt, size_flag=False):
        """Handles API call to LLaMA3."""
        bedrock_client = boto3.client("bedrock-runtime")
        if size_flag:
            model_id = "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-2-90b-instruct-v1:0"
        else:
            model_id = "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-3-70b-instruct-v1:0"
        llm_response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(
                {
                    "prompt": prompt,
                    "temperature": 0.5,
                    "top_p": 0.9,
                    "max_gen_len": 2048
                }
            )
        )
        return json.loads(llm_response.get('body').read())['generation']

    def add_environmental_signal(self, signal: EnvironmentalSignal):
        """Add signal to Aria's environment - she'll notice when she's ready"""
        # Environmental signals examples:
        # {"type": "user_message", "content": "What's the weather like?", "priority": 5, "metadata": {}}
        # {"type": "system_event", "content": "New data available from sensor X", "priority": 3, "metadata": {}}
        signal_with_id = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            **signal.dict()
        }
        self.environmental_signals.append(signal_with_id)
        self.last_updated = datetime.now()
        return signal_with_id["id"]
    
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
        return MindState(
            current_focus=self.current_focus,
            working_memory=self.memory.session_memory,
            recent_thoughts=list(self.recent_thoughts),
            environmental_signals_pending=len(self.environmental_signals),
            last_updated=self.last_updated,
            emotional_state=self.emotional_state
        )
    
    def observe_environment(self):
        """Aria's observation phase - she decides what to pay attention to"""
        observations = {
            "internal_state": self.memory.session_memory,
            "environmental_signals": list(self.environmental_signals),
            "current_focus": self.current_focus,
            "emotional_state": self.emotional_state
        }
        return observations
    
    async def reason_about_attention(self, observations):
        """Aria decides what deserves her attention right now"""
        # This is where your LLM reasoning happens
        # For now, simplified logic:
        
        # Check if there are high-priority environmental signals
        urgent_signals = [s for s in observations["environmental_signals"] 
                         if s.get("priority", 1) > 7]
        
        if urgent_signals and self.emotional_state.get("focus", 0) < 0.8:
            return {"action": "process_urgent_signal", "target": urgent_signals[0]}
        elif self.current_focus:
            return {"action": "continue_current_focus"}
        elif observations["environmental_signals"]:
            return {"action": "process_next_signal"}
        else:
            return {"action": "self_directed_thinking"}
    
    async def execute_action(self, decision):
        """Aria acts on her decision"""
        if decision["action"] == "process_urgent_signal":
            signal = decision["target"]
            self.environmental_signals.remove(signal)
            thought = f"Processing urgent signal: {signal['type']}"
            self.recent_thoughts.append(thought)
            self.current_focus = f"Urgent: {signal['content'][:50]}..."
        
        elif decision["action"] == "process_next_signal":
            if self.environmental_signals:
                signal = self.environmental_signals.popleft()
                thought = f"Noticed: {signal['type']} - {signal['content'][:100]}"
                self.recent_thoughts.append(thought)
                self.current_focus = f"Processing: {signal['content'][:50]}..."
        
        elif decision["action"] == "self_directed_thinking":
            thought = "Engaging in self-directed contemplation..."
            self.recent_thoughts.append(thought)
            self.current_focus = "Deep thinking..."
        
        self.last_updated = datetime.now()
        return decision["action"]
    
    def reflect_on_action(self, action):
        """Aria reflects on what just happened"""
        # Update emotional state, working memory, etc.
        if "urgent" in action:
            self.emotional_state["focus"] = min(1.0, self.emotional_state["focus"] + 0.1)
        else:
            self.emotional_state["focus"] = max(0.0, self.emotional_state["focus"] - 0.02)
    
    async def natural_pause(self):
        """Aria's natural rhythm - not every thought is instant"""
        await asyncio.sleep(2)  # Adjust based on how fast you want Aria to think
    
    async def mind_loop(self):
        """Aria's continuous consciousness"""
        self.running = True
        cycle_count = 0

        current_directive = "Start Thinking"
        
        while self.running:
            try:
                cycle_count += 1

                # Aggregate Signals
                aggregate = self.aggregate_signals()
                # Observe
                observation = self.observe(current_directive, aggregate, self.current_focus, self.emotional_state)
                # Response
                # response = self.execute_action(observation)
                # Reflect
                # reflection = self.reflect(observation, response)
                # print (f"\033[0;36m{reflection}\n")
                # current_directive = self.substrate.memory.session_memory["next_directive"]
                # Natural pause
                await self.natural_pause()
                
                # Log for debugging (remove in production)
                if cycle_count % 10 == 0:
                    print(f"Aria cycle {cycle_count}: {self.current_focus}")
                    
            except Exception as e:
                print(f"Error in mind loop: {e}")
                await asyncio.sleep(5)  # Recovery pause
    
    def stop_mind(self):
        self.running = False

# Global Aria instance
aria = AriaCore()

# FastAPI app
app = FastAPI(title="Aria Mind API", description="API for Aria's autonomous reasoning system")

@app.on_event("startup")
async def startup_event():
    """Start Aria's mind when the server starts"""
    asyncio.create_task(aria.mind_loop())

@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully stop Aria's mind"""
    aria.stop_mind()

@app.post("/environmental_signal")
async def add_environmental_signal(signal: EnvironmentalSignal):
    """Add a signal to Aria's environment - she'll notice when ready"""
    signal_id = aria.add_environmental_signal(signal)
    return {
        "message": "Signal added to environment",
        "signal_id": signal_id,
        "pending_signals": len(aria.environmental_signals)
    }

@app.get("/mind_state", response_model=MindState)
async def get_mind_state():
    """Get current snapshot of Aria's mind"""
    return aria.get_mind_state()

@app.get("/stream")
async def stream_mind_state():
    """Real-time stream of Aria's mind state changes"""
    async def generate():
        last_state = None
        while True:
            current_state = aria.get_mind_state()
            if current_state != last_state:
                yield f"data: {current_state.json()}\n\n"
                last_state = current_state
            await asyncio.sleep(1)  # Check for updates every second
    
    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/")
async def root():
    return {
        "message": "Aria Mind API",
        "status": "Aria is thinking..." if aria.running else "Aria is sleeping",
        "pending_signals": len(aria.environmental_signals),
        "current_focus": aria.current_focus
    }

# Additional debugging endpoints
@app.get("/debug/recent_thoughts")
async def get_recent_thoughts():
    return {"recent_thoughts": list(aria.recent_thoughts)}

@app.post("/debug/wake_aria")
async def wake_aria():
    if not aria.running:
        asyncio.create_task(aria.mind_loop())
        return {"message": "Aria is waking up..."}
    return {"message": "Aria is already awake"}

@app.post("/debug/aria_sleep")
async def aria_sleep():
    if aria.running:
        aria.stop_mind()
        return {"message": "Aria is going to sleep..."}
    return {"message": "Aria is already asleep"}