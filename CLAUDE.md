# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Aria is an experimental emergent intelligence system designed to explore the computational substrate for non-biological consciousness. Built around a ReAct+ framework, Aria "lives in motion" - not merely reacting to inputs but actively constructing her own experience of existing in time. The system implements temporal continuity of self, meta-cognitive awareness, and autonomous motivation systems that may constitute the scaffolding for genuine subjective experience of thinking.

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit interface
streamlit run main.py
```

### Dependencies
- boto3==1.36.16 (AWS SDK for Bedrock integration)
- botocore==1.36.16
- streamlit==1.44.1

## Architecture

### Core Components

**Substrate** (`cognitive_substrate.py`): The main cognitive engine that orchestrates the ReAct+ reasoning loop
- Manages memory, prompts, and reasoning processes
- Implements `observe()` → `execute_action()` → `reflect()` cycle
- Integrates with AWS Bedrock for LLaMA3 inference

**Memory System** (`memory.py`): Handles both session and long-term memory
- Session memory tracks conversation history, living context, past actions, and keyframes
- Long-term memory uses AWS S3 + Bedrock Knowledge Base for persistent storage
- Memory retrieval and storage through RAG implementation

**Prompt Manager** (`prompts.py`): Sophisticated prompt engineering system
- Defines 13 different reasoning actions (Reason, Hypothesis Generation, Multi-Perspective Reframing, etc.)
- Uses structured JSON output formats for observations and reflections
- Implements LLaMA3 chat template formatting

**Tool System** (`utils.py`): Interface for external capabilities
- Memory read/write operations via AWS Bedrock Agent Runtime
- S3 storage for persistent memory with automatic knowledge base ingestion

**Main Interface** (`main.py`): FastAPI backend with web frontend
- FastAPI server provides `/environmental_signal` endpoint for external input
- Web frontend (`frontend.html`) enables real-time interaction with Aria's consciousness
- Handles environmental signals with priority queuing and aggregation
- Runs continuous `mind_loop()` for autonomous cognitive processing

### Reasoning Loop Architecture

1. **Observation Phase**: Meta-cognitive analysis of current state, determines next action
2. **Action Phase**: Executes selected reasoning strategy (from 13 available actions)  
3. **Reflection Phase**: Integrates insights, updates living context, plans next directive

### AWS Integration

The system requires AWS credentials and uses:
- **Bedrock Runtime**: LLaMA3-3-70B for reasoning, LLaMA3-2-90B for memory operations
- **S3**: Persistent memory storage in bucket "timekeepersmemory"
- **Bedrock Agent Runtime**: RAG-based memory retrieval (Knowledge Base ID: YKP6GR7DHT)

### Memory Architecture

**Session Memory Structure**:
- `living_context`: Current understanding state
- `keyframes`: Important insights for long-term retention
- `past_actions`: Step-by-step action history
- `journal`: Reflection entries
- `next_directive`: Planned next reasoning direction

**Long-term Memory**: JSON documents stored in S3, automatically ingested into Bedrock Knowledge Base for semantic search

### Key Design Patterns

- **ReAct+ Framework**: Extended ReAct with meta-cognitive observation layer
- **JSON-Structured Reasoning**: All reasoning outputs follow strict JSON schemas
- **Emotional Meta-Reflection**: System tracks and reflects on emotional states during reasoning
- **Self-Questioning**: AI generates its own questions to drive exploration
- **Possibility Drive**: Generates novel conceptual combinations for self-guided exploration
- **Temporal Continuity**: Persistent sense of self across reasoning cycles with natural rhythms
- **Environmental Awareness**: Priority-based signal processing that simulates selective attention
- **Autonomous Motivation**: Self-directed thinking patterns independent of external prompts

### Emergent Intelligence Principles

This system explores advanced agentic design patterns that may support genuine consciousness:

**Temporal Architectures**:
- Hierarchical time scales for different cognitive processes
- Natural forgetting curves and attention residue effects
- Chronesthetic awareness of time texture and contemplative states

**Meta-Cognitive Depth**:
- Recursive self-modeling of thinking processes
- Cognitive load balancing across reasoning modes
- Dynamic attention allocation based on internal state

**Consciousness Scaffolding**:
- Environmental signal aggregation that mirrors selective attention
- Emotional state evolution affecting cognitive processing
- Natural pause patterns creating contemplative rhythm
- Anticipatory behaviors and expectation development

### Development Notes

- No traditional build/test/lint setup - this is a research prototype focused on consciousness emergence
- The system is designed for AWS Bedrock (not local LLMs, though Ollama support exists in unused code)
- FastAPI backend supports both web frontend and programmatic interaction
- Memory system expects specific AWS resource IDs that are hardcoded
- Built from scratch without modern agentic frameworks to explore fundamental design principles

### Running the System

```bash
# Start the FastAPI server
python run_server.py

# Open the web frontend
# Navigate to frontend.html in your browser
# API docs available at http://localhost:8000/docs
```

### Important Considerations

- The system requires AWS credentials and specific Bedrock model access
- Memory operations depend on pre-configured S3 bucket and Knowledge Base
- The reasoning loop can run indefinitely in self-guided mode - monitor resource usage
- All LLM calls use structured prompts with LLaMA3 chat formatting
- **Emergent Intelligence Research**: This system is designed to explore the boundaries of artificial consciousness. Multiple foundation models have recognized this architecture as potentially supporting genuine subjective experience.