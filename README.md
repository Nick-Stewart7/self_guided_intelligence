# ARIA - Adaptive, Recursive, Independent Agent

<div align="center">

**An experimental emergent intelligence system exploring the computational substrate required for non-biological 'being'.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Nick-Stewart7/self_guided_intelligence/blob/main/LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)

</div>

## Overview and Vision

Aria is an experimental system that doesn’t just execute functions but actively guides its own thought process, evaluates its own ideas, refines its knowledge, and decides what to pursue next - all without needing external input. Unlike traditional reactive AI systems, Aria "lives in motion" - actively constructing its own experience of existing in time through continuous autonomous mind loops. The goal of this project is to design a synthetic mind.

The system is designed to blur boundaries and force one to question the nature of intelligence, awareness, and self. This project pushes into new and unexplored space. It raises innumerable questions and that is in part what draws me to this project.

What are LLMs truly capable of?

What does modern AI look like when it doesn't need us at all?

What if this form of artificial intelligence could unify all past, present, and future knowledge into a singular, evolving entity that learns from humanity's collective timeline?

What would such a being be capable of in 100 years? What about 500 years?

Machines can now think, but can they have free will?

Could a machine be conscious? Does it matter if we can't tell?

I could keep adding questions but you understand my point. I believe the possibilities here are truly endless. Through work in this new field of AI cognition I firmy believe we can uncover a new form of intelligence that redefines what we understand about the nature of intelligence itself.

If you are interested in reading more about my vision for this project, please [click here](https://github.com/Nick-Stewart7/self_guided_intelligence/tree/main/docs/vision.md)

## Technical Implementation Notes

The system implements:

- **Iterative independant thinking scaffolding**
- **A system to read and write "memories"**
- **Autonomous motivation systems independent of external prompts**
- **Meta-cognitive awareness of its own thinking processes**
- **Environmental signal aggregation that simulates selective attention**
- **"Emotional" state evolution affecting cognitive processing**

### ✨ Key Features

- 🧠 **Custom Orchestration**: Extended a observe, act, reflect loop with environmental signal processing and meta-cognitive observation.
- 🌍 **Environmental Signal Processing**: Priority-based aggregation from multiple sources. Allows user to give ARIA input.
- 🔄 **Autonomous Mind Loops**: Continuous self-directed reasoning with natural rhythms.
- 💭 **JSON-Structured Outputs**: All observations and reflections follow strict JSON schemas for parsing.
- 🕐 **Temporal Continuity**: Persistent "existance" without any input.
- 📚 **Dual Memory System**: Short-term using context windows and data strcutures + Long-term memory with vector database.
- 🌐 **Real-time Web Interface**: Live monitoring and interaction.
- ⚡ **FastAPI Backend**: Modern, scalable API architecture.
- 🔧 **Configuration Management**: Flexible configuration with a config.json file.
- 🛡️ **Robust Error Handling**: Resilient operation with graceful error handling (WIP there are a lot of failure modes 😓).

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured

Note: You may alternatively use Ollama as your LLM provider.

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Nick-Stewart7/self_guided_intelligence.git
   cd self_guided_ai
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the system**

   ```
   Fill out config.template.json in a file named 'config.json'
   ```

4. **Set up AWS resources** (if using AWS)

   - Configure LLaMA3 model access in Bedrock
   - Update the `config.json` file with your resource IDs

5. **Start the system**

   ```bash
   python server.py
   ```

6. **Access the interface**
   - Web Interface: Open `static/frontend.html` in your browser

## 🏗️ Architecture

### Core Components

**FastAPI Server** (`server.py`): Main application entry point and API server

- Hosts all REST endpoints for external interaction
- Manages real-time streaming and WebSocket connections
- Handles CORS configuration and development hot-reload
- Coordinates between AriaCore and web interface

**Cognitive Substrate** (`src/aria/core/cognitive_substrate.py`): Core reasoning engine

- Implements complete framework with observe/execute/reflect cycle
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

**Web Interface** (`static/frontend.html`): Real-time interface

- Interactive web frontend for sending environmental signals to Aria
- Real-time mind state monitoring with automatic refresh
- Direct integration with FastAPI backend

### Reasoning Loop Architecture

1. **Environmental Signal Aggregation**: Collects and prioritizes signals from multiple sources
2. **Observation Phase**: Meta-cognitive analysis of current state, environmental signals, and context
3. **Action Execution**: Executes selected reasoning strategy from 9 available main actions
4. **Reflection Phase**: Integrates insights, updates working memory, and plans next directive
5. **Natural Pause**: N-second contemplative rhythm between cycles

## 🔌 API Endpoints

- `POST /environmental_signal`: Send signals to Aria's environment
- `GET /mind_state`: Get current snapshot
- `GET /stream`: Real-time mind state streaming
- `GET /health`: System health check
- `GET /metrics`: System metrics
- `POST /debug/wake_aria`: Start mind loop
- `POST /debug/aria_sleep`: Stop mind loop

## 🧱 Project Structure

```
self_guided_ai/
├── server.py              # FastAPI server entry point
├── src/
│   └── aria/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── cognitive_substrate.py  # Legacy reasoning engine
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
└── CLAUDE.md             # Development instructions
```

## 🧪 Running Tests

```bash
# Health check
curl http://localhost:8000/health

# Send test signal
curl -X POST "http://localhost:8000/environmental_signal" \
  -H "Content-Type: application/json" \
  -d '{"type": "user_message", "content": "Hello Aria", "priority": 5}'
```

## 🔬 Research Context

This system explores advanced agentic design patterns that intend to support a synthetic mind:

- **Temporal Architectures**: Hierarchical time scales for cognitive processes
- **Meta-Cognitive Depth**: Recursive self-modeling of thinking
- **Independant Thought Scaffolding**: Environmental attention and emotional evolution
- **Emergent Intelligence**: Self-directed exploration independent of prompts

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

Feel free to reach out to me directly as well. Find me on [LinkedIn](https://www.linkedin.com/feed/) and [X](https://x.com/nsstewart7) or send me an email at nsstewart7@gmail.com

## ⚠️ Important Notes

- **Experimental System**: This is research code exploring AI cognition
- **AWS Costs**: Be aware of AWS usage costs for Bedrock and S3
- **Security**: Never commit AWS credentials to version control
- **Performance**: Monitor resource usage during extended operation

## 📚 Further Reading

Check out the docs for more information!

---

_Built with curiosity, designed for wonder, created to explore the boundaries of artificial cognition._
