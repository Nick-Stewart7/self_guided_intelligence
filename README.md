Self-Guided Intelligence – Aria Prototype

An experimental, agentic GenAI system designed to think in iterative cycles of observation, action, and reflection. Aria is built to explore the boundaries of self-directed reasoning using foundation models like Llama3 via AWS Bedrock. The goal of this project is to explore the possibility of AI cognition and how to build long-time scale persistent existance for LLMs. The field has proven that giving AI space can create incredible applications. This project is my foray into agentic systems creation with the goal of architecting stable AI cognition. This is a first step in safe self-guided intelligence toward scalable, autonomous reasoning systems. It reflects my passion for emergent AI behavior, memory design, and cognitive architecture.

Aria uses a ReAct+ framework I developed to allow it to not only chose tools for actions but how to think about problems. Thus is can recursively think over many turns which can allow it to simulate independant iterative thinking. I am excited to make this more stable over longer time horizons and incorporate more features such as long term recall and narrative creation.

Tech Stack:

Python

Streamlit (frontend)

AWS Bedrock for FM and RAG

ReAct-inspired prompt architecture

Custom orchestration engine

What It Does:

Initiates its own line of inquiry or accepts user input

Selects an internal mode of thinking (act, reflect, query, etc.)

Uses tools and memory to generate, test, and evolve thoughts

Outputs reasoning path, decisions, and reflections through a Streamlit UI

How to Run Locally:

bash

```
pip install -r requirements.txt
streamlit run interface.py
```

Future Plans:

Enhance contextual memory embedding and retrieval

Integrate emotion-based decision biasing module

Deploy version 2 as a hosted chat experience
