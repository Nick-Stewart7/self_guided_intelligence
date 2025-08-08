# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Aria is an experimental self-guided AI system that implements a ReAct+ framework for iterative reasoning. The system is designed to think in cycles of observation, action, and reflection, with the ability to recursively think over many turns to simulate independent iterative thinking.

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

**Main Interface** (`main.py`): Streamlit frontend
- Handles user input queue and displays AI thoughts
- Runs both reactive (user input) and proactive (self-guided) reasoning modes

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

### Development Notes

- No traditional build/test/lint setup - this is a research prototype
- The system is designed for AWS Bedrock (not local LLMs, though Ollama support exists in unused code)
- Streamlit provides the user interface but the core can run headlessly
- Memory system expects specific AWS resource IDs that are hardcoded

### Important Considerations

- The system requires AWS credentials and specific Bedrock model access
- Memory operations depend on pre-configured S3 bucket and Knowledge Base
- The reasoning loop can run indefinitely in self-guided mode - monitor resource usage
- All LLM calls use structured prompts with LLaMA3 chat formatting