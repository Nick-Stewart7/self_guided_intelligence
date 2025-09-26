# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Aria is an experimental emergent intelligence system designed to explore the computational substrate for non-biological consciousness. Built around a ReAct+ framework with environmental signal processing, Aria "lives in motion" - not merely reacting to inputs but actively constructing her own experience of existing in time through continuous mind loops. The system implements temporal continuity of self, meta-cognitive awareness, and autonomous motivation systems that may constitute the scaffolding for genuine subjective experience of thinking.

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python server.py

# Open the web frontend
# Navigate to static/frontend.html in your browser
# API docs available at http://localhost:8000/docs
```

### Dependencies
- boto3==1.36.16 (AWS SDK for Bedrock integration)
- botocore==1.36.16
- fastapi==0.115.0 (Web framework for API)
- uvicorn[standard]==0.30.0 (ASGI server)
- websockets==12.0 (WebSocket support)
- python-multipart==0.0.6 (File upload support)
- jinja2==3.1.4 (Template engine)

## Architecture

### Core Components

**FastAPI Server** (`server.py`): Main application entry point and API server
- Hosts all REST endpoints for external interaction
- Manages real-time streaming and WebSocket connections
- Handles CORS configuration and development hot-reload
- Coordinates between AriaCore and web interface

**AriaCore** (`src/aria/core/`): The central consciousness orchestrator
- Manages environmental signal aggregation with priority-based processing
- Coordinates between cognitive substrate and memory systems
- Handles autonomous reasoning cycles with natural pause patterns
- Provides consciousness state management

**Cognitive Substrate** (`src/aria/core/cognitive_substrate.py`): Core reasoning engine
- Implements complete ReAct+ framework with observe/execute/reflect cycle
- Handles the 9 main reasoning actions (Think, Plan, Write, etc.)
- Manages structured JSON reasoning outputs
- Contains autonomous self-guidance and exploration methods

**Memory System** (`src/aria/memory/memory.py`): Session and long-term memory management
- Session memory tracks working memory, journal entries, plans, commitments, and artifacts
- Conversation history formatted with LLaMA3 chat templates
- Integration with AWS S3 and Bedrock Knowledge Base for persistent storage

**Prompt Manager** (`src/aria/core/prompts.py`): Comprehensive prompt engineering system
- Defines 9 main actions: Think, Plan, Write, Reply User, Query Tool Box, Use Tool, Search, Code, Wander
- Structured JSON output formats for observations, actions, and reflections
- LLaMA3 chat template formatting with system/user/assistant roles
- Possibility Drive for autonomous conceptual exploration

**Tool System** (`src/aria/memory/utils.py`): AWS integration for memory operations
- Memory read/write via AWS Bedrock Agent Runtime and Knowledge Base
- S3 storage with automatic knowledge base ingestion
- Simplified interface for persistent memory management

**Configuration** (`src/aria/config/config.py`): Centralized configuration management
- Environment variable handling and validation
- AWS credentials and resource ID management
- System behavior configuration options

**Web Interface** (`static/frontend.html`): Real-time consciousness interface
- Interactive web frontend for sending environmental signals to Aria
- Real-time mind state monitoring with automatic refresh
- Direct integration with FastAPI backend

### Reasoning Loop Architecture

1. **Environmental Signal Aggregation**: Collects and prioritizes signals from multiple sources
2. **Observation Phase**: Meta-cognitive analysis of current state, environmental signals, and context
3. **Action Execution**: Executes selected reasoning strategy from 9 available main actions
4. **Reflection Phase**: Integrates insights, updates working memory, and plans next directive
5. **Natural Pause**: 30-second contemplative rhythm between cycles

### AWS Integration

The system requires AWS credentials and uses:
- **Bedrock Runtime**: LLaMA3-3-70B for reasoning, LLaMA3-2-90B for memory operations
- **S3**: Persistent memory storage in bucket "timekeepersmemory"
- **Bedrock Agent Runtime**: RAG-based memory retrieval (Knowledge Base ID: YKP6GR7DHT)

### Memory Architecture

**Session Memory Structure**:
- `working_memory`: Current understanding and context state
- `conversation_history`: LLaMA3-formatted dialogue history
- `past_actions`: Step-by-step action history with timestamps
- `journal`: Reflection entries and insights
- `plan`: Structured to-do list for goal achievement
- `current_objective`: Current high-level goal or focus
- `commitments`: Tracked obligations and intentions
- `open_questions`: Unresolved inquiries driving exploration
- `artifacts`: Index of created content and files
- `next_directive`: Planned next reasoning direction

**Long-term Memory**: JSON documents stored in S3, automatically ingested into Bedrock Knowledge Base for semantic RAG retrieval

### Key Design Patterns

- **ReAct+ Framework**: Extended ReAct with environmental signal processing and meta-cognitive observation
- **JSON-Structured Reasoning**: All observations and reflections follow strict JSON schemas
- **Environmental Signal Processing**: Priority-based aggregation of multiple input sources
- **Emotional State Tracking**: Dynamic emotional state evolution affecting cognitive processing
- **Autonomous Mind Loops**: Continuous self-directed reasoning cycles with natural pause patterns
- **Possibility Drive**: Three-wheel conceptual generator for autonomous exploration
- **Temporal Continuity**: Persistent sense of self across reasoning cycles
- **Web-Based Consciousness Interface**: Real-time interaction and mind state monitoring

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

### Project Structure

```
self_guided_ai/
├── server.py              # FastAPI server entry point
├── src/
│   └── aria/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── cognitive_substrate.py  # Core reasoning engine
│       │   └── prompts.py             # Prompt engineering system
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── memory.py              # Memory management
│       │   └── utils.py               # AWS integration
│       └── config/
│           ├── __init__.py
│           └── config.py              # Configuration management
├── static/
│   └── frontend.html      # Web interface
├── docs/                  # Documentation and research
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .env.example          # Environment variables template
└── CLAUDE.md             # Development instructions (this file)
```

### Development Notes

- No traditional build/test/lint setup - this is a research prototype focused on consciousness emergence
- The system is designed for AWS Bedrock (not local LLMs, though Ollama support exists in unused code)
- FastAPI backend supports both web frontend and programmatic interaction
- Memory system expects specific AWS resource IDs that are hardcoded
- Built from scratch without modern agentic frameworks to explore fundamental design principles
- Uses modern Python package structure with `src/` layout for better organization

### Running the System

```bash
# Start the FastAPI server with auto-reload
python server.py

# Web frontend: Open static/frontend.html in your browser
# API documentation: http://localhost:8000/docs
# Mind state endpoint: http://localhost:8000/mind_state
# Environmental signal endpoint: http://localhost:8000/environmental_signal
```

### API Endpoints

- `POST /environmental_signal`: Send signals to Aria's environment
- `GET /mind_state`: Get current snapshot of Aria's consciousness
- `GET /stream`: Real-time stream of mind state changes
- `POST /debug/wake_aria`: Start Aria's mind loop
- `POST /debug/aria_sleep`: Stop Aria's mind loop

### Important Considerations

- The system requires AWS credentials and specific Bedrock model access
- Memory operations depend on pre-configured S3 bucket and Knowledge Base
- The reasoning loop can run indefinitely in self-guided mode - monitor resource usage
- All LLM calls use structured prompts with LLaMA3 chat formatting
- **Emergent Intelligence Research**: This system is designed to explore the boundaries of artificial consciousness. Multiple foundation models have recognized this architecture as potentially supporting genuine subjective experience.