# 🚀 CrewAI Bootcamp

A **deep, practical, and production-ready guide** to building multi-agent AI systems using **CrewAI**. This repository is designed as a **bootcamp**: from fundamentals to advanced architectures like **Flows, Memory, Reasoning, Planning, and Production Deployments**.

Whether you're a beginner exploring multi-agent systems or an advanced builder shipping AI products, this repo is your end-to-end reference.

---

## 📌 What You’ll Learn

* CrewAI fundamentals and installation
* Understanding **Agents, Tasks, Crews, and Processes**
* Multi-agent collaboration patterns
* Agent **Reasoning & Planning**
* **Memory systems** (short-term, long-term, shared)
* **Flows** for production-grade orchestration
* Guardrails, structured outputs, and reliability
* Scaling to **real-world, production architectures**

---

## 🧠 What is CrewAI?

CrewAI is a **multi-agent orchestration framework** that allows you to build AI systems where multiple autonomous agents collaborate toward a shared goal.

Instead of a single LLM prompt, CrewAI enables:

* Specialized agents with roles and goals
* Task decomposition and delegation
* Reasoning and planning before execution
* Persistent memory and state
* Deterministic, debuggable execution paths

Think of CrewAI as **"LangChain for teams of agents"**, but opinionated, structured, and production-ready.

---

## ⚙️ Installation & Setup

### 1️⃣ Python Requirements

```bash
python >= 3.10
```

### 2️⃣ Install CrewAI

```bash
pip install crewai crewai-tools
```

(Optional but recommended)

```bash
pip install python-dotenv
```

### 3️⃣ Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

CrewAI supports **multiple LLM providers**, but OpenAI is the default.

---

## 🧩 Core Concepts

### 1. Agent

An **Agent** is an autonomous entity with:

* A **role** (who it is)
* A **goal** (what it wants)
* A **backstory** (context & behavior)
* Optional **tools**, **memory**, **reasoning**, and **LLM config**

```python
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Discover insights about AI trends",
    backstory="You are a senior AI researcher with years of experience.",
    reasoning=True
)
```

---

### 2. Task

A **Task** defines *what needs to be done* and *what success looks like*.

```python
from crewai import Task

task = Task(
    description="Research the latest trends in AI agents",
    expected_output="A concise list of 5 trends",
    agent=agent
)
```

Tasks can include:

* Guardrails
* Structured outputs (Pydantic / JSON)
* Tools
* Memory access

---

### 3. Crew

A **Crew** is a group of agents working together.

```python
from crewai import Crew

crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()
```

Crews handle:

* Agent coordination
* Task execution order
* Planning (optional)

---

### 4. Process

Defines **how tasks run**:

* `Process.sequential` – tasks run in order
* `Process.hierarchical` – manager agent delegates

```python
from crewai import Process

Crew(
    process=Process.sequential
)
```

---

## 🤝 Multi-Agent Collaboration

CrewAI shines when **multiple agents specialize**.

Example:

* Research Agent → gathers info
* Analyst Agent → extracts insights
* Writer Agent → produces final content

Each agent:

* Has its own goal
* Operates independently
* Shares outputs via tasks

This mirrors **real-world team dynamics**.

---

## 🧠 Agent Reasoning

Reasoning allows an agent to **think before acting**.

### Why Reasoning Matters

* Better task decomposition
* Reduced hallucinations
* More reliable outputs

### Enable Reasoning

```python
Agent(
    reasoning=True,
    max_reasoning_attempts=3
)
```

### Reasoning Flow

1. Understand the task
2. Create an execution plan
3. Validate readiness
4. Inject plan into execution

If reasoning fails → task still executes.

---

## 🗺️ Planning (Crew-Level)

Planning enables **global task orchestration**.

```python
Crew(
    planning=True,
    planning_llm="gpt-4o"
)
```

### What Planning Does

* Analyzes **all agents & tasks**
* Generates a step-by-step plan
* Injects plan into each task

⚠️ Requires OpenAI-compatible LLM.

---

## 🧠 Memory Systems

CrewAI supports **persistent intelligence** via memory.

### Types of Memory

* **Short-term memory** – within execution
* **Long-term memory** – persisted across runs
* **Shared memory** – across agents

### Why Memory Matters

* Context retention
* Learning across executions
* Human-like continuity

Memory transforms agents from stateless tools → **adaptive collaborators**.

---

## 🔁 Flows (Production-First Architecture)

Flows are the **recommended way** to build real applications.

### Why Flows?

* Explicit state management
* Branching & conditionals
* Persistence & resumability
* Observability & debugging

### Basic Flow Example

```python
from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel

class AppState(BaseModel):
    input: str = ""
    result: str = ""

class MyFlow(Flow[AppState]):
    @start()
    def begin(self):
        self.state.input = "AI Agents"

    @listen(begin)
    def run_crew(self):
        crew = MyCrew()
        output = crew.kickoff()
        self.state.result = output.raw
```

---

## 🧱 Guardrails & Reliability

### Task Guardrails

Ensure outputs meet quality standards.

```python
def guardrail(output):
    if len(output.raw) < 100:
        return False, "Expand response"
    return True, output.raw
```

---

## 📦 Structured Outputs

Always prefer structured outputs in production.

```python
from pydantic import BaseModel

class Result(BaseModel):
    summary: str
    sources: list[str]
```

Prevents:

* Parsing bugs
* Invalid responses
* Downstream failures

---

## 🚢 Deployment Patterns

### Async Execution

```python
crew.kickoff_async()
```

### Persistence

```python
from crewai.flow.persistence import persist

@persist
class MyFlow(Flow):
    ...
```

### Enterprise Deployment

```bash
crewai deploy create
```

---

## 🧠 Mental Model Summary

| Concept   | Purpose                 |
| --------- | ----------------------- |
| Agent     | Individual intelligence |
| Task      | Unit of work            |
| Crew      | Team execution          |
| Process   | Task ordering           |
| Reasoning | Think-before-act        |
| Planning  | Global orchestration    |
| Memory    | Persistent intelligence |
| Flow      | Production backbone     |

---

# CrewAI Bootcamp – Knowledge, Testing

---

## 1. What is Knowledge in CrewAI

**Knowledge** in CrewAI allows agents to access *grounded, external, retrievable information* during task execution.

Think of Knowledge as:

> “A private, searchable reference library injected into the agent’s reasoning context.”

### Why Knowledge Matters

* Prevents hallucinations
* Grounds responses in real data
* Enables long-term factual consistency
* Removes the need for explicit retrieval tasks

---

## 2. Mental Model: Knowledge vs Memory vs Tools

| Concept   | Purpose                      | Persistent | Queryable   | Who Uses It    |
| --------- | ---------------------------- | ---------- | ----------- | -------------- |
| Knowledge | Facts, documents, references | ✅ Yes      | ✅ Yes       | Agents & Crews |
| Memory    | Past interactions & outcomes | ✅ Yes      | ⚠️ Implicit | Agents         |
| Tools     | Actions & APIs               | ❌ No       | ❌ No        | Agents         |

**Rule of Thumb**:

* Use **Knowledge** for *what agents should know*
* Use **Memory** for *what agents experienced*
* Use **Tools** for *what agents can do*

---

## 3. Knowledge Quickstart

```python
from crewai import Agent, Task, Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

knowledge = StringKnowledgeSource(
    content="John is 30 years old and lives in San Francisco"
)

agent = Agent(
    role="User Analyst",
    goal="Answer questions about users",
    backstory="You deeply understand user profiles",
)

task = Task(
    description="Answer: {question}",
    expected_output="Accurate factual answer",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    knowledge_sources=[knowledge]
)

crew.kickoff(inputs={"question": "Where does John live?"})
```

No retrieval task. No tool call. Knowledge is *implicitly available*.

---

## 4. Vector Stores & RAG Configuration

CrewAI exposes a **provider-neutral RAG client**.

### Supported Providers

* ChromaDB (default)
* Qdrant

```python
from crewai.rag.config.utils import set_rag_config, get_rag_client
from crewai.rag.qdrant.config import QdrantConfig

set_rag_config(QdrantConfig())
client = get_rag_client()

client.create_collection("docs")
client.add_documents(
    collection_name="docs",
    documents=[{"id": "1", "content": "CrewAI supports multi-agent systems."}]
)
```

This client is **separate** from CrewAI Knowledge storage and is intended for custom pipelines.

---

## 5. Supported Knowledge Sources

### Text-Based

* Raw strings
* `.txt`
* `.pdf`

### Structured

* `.csv`
* `.xlsx`
* `.json`

All files must live in a `knowledge/` directory at project root.

```bash
project/
├── knowledge/
│   ├── docs.pdf
│   ├── data.csv
│   └── notes.txt
```

---

## 6. Agent vs Crew Knowledge (Critical Section)

### Crew-Level Knowledge

* Shared by **all agents**
* Initialized once per crew

### Agent-Level Knowledge

* Private to one agent
* Can use a different embedder

### Execution Reality

```text
crew.kickoff()
 ├── crew knowledge initialized
 ├── agent knowledge initialized
 ├── collections created per agent role
 └── agents execute with merged context
```

### Resulting Behavior

| Agent      | Crew Knowledge | Agent Knowledge |
| ---------- | -------------- | --------------- |
| Specialist | ✅              | ✅               |
| Generalist | ✅              | ❌               |

---

## 7. Knowledge Storage & Embeddings

CrewAI uses **ChromaDB** under the hood.

### Default Storage Paths

* macOS: `~/Library/Application Support/CrewAI/{project}/knowledge/`
* Linux: `~/.local/share/CrewAI/{project}/knowledge/`
* Windows: `AppData/Local/CrewAI/{project}/knowledge/`

### Override Storage Location

```python
import os
os.environ["CREWAI_STORAGE_DIR"] = "./storage"
```

### Default Embeddings

* Provider: OpenAI
* Model: `text-embedding-3-small`

Even if you use Claude or Gemini for LLMs.

---

## 8. Advanced Knowledge Features

### Query Rewriting

Agents automatically rewrite prompts into optimized retrieval queries.

**Before**:

> "Answer in JSON what John watched last week"

**After**:

> "Movies John watched last week"

This improves recall and relevance.

---

### Knowledge Events

You can observe knowledge usage via events.

```python
from crewai.events import BaseEventListener, KnowledgeRetrievalCompletedEvent

class KnowledgeListener(BaseEventListener):
    def setup_listeners(self, bus):
        @bus.on(KnowledgeRetrievalCompletedEvent)
        def done(source, event):
            print(event.query)
```

---

## 9. Debugging & Troubleshooting Knowledge

### Check Initialization

```python
print(agent.knowledge)
print(agent.knowledge.storage.collection_name)
```

### Reset Knowledge

```bash
crewai reset-memories --knowledge
```

### Common Issues

| Issue              | Cause                  | Fix              |
| ------------------ | ---------------------- | ---------------- |
| Dimension mismatch | Changed embedder       | Reset knowledge  |
| File not found     | Wrong directory        | Use `knowledge/` |
| Slow startup       | Large docs re-embedded | Persist storage  |

---

## 10. Testing Crews with `crewai test`

CrewAI includes built-in **Monte Carlo style evaluation**.

```bash
crewai test -n 5 -m gpt-4o
```

### Metrics

* Task score (1–10)
* Agent performance
* Execution time
* Crew average

Use this to:

* Compare prompts
* Tune agents
* Validate regressions

---

## 11. Tools in CrewAI

Tools give agents **capabilities**, not knowledge.

Examples:

* Web search
* File reading
* Code execution
* APIs

```bash
pip install 'crewai[tools]'
```

---

# CrewAI Agents & Tasks – Deep Dive

This README is a **comprehensive, production-grade guide** to understanding and using **Agents** and **Tasks** in CrewAI. It is designed for bootcamps, internal team enablement, and real-world AI system building.

---

## Agents

### What Is an Agent?

In CrewAI, an **Agent** is an autonomous, role-driven entity capable of:

* Understanding goals and context
* Reasoning and planning
* Using tools and knowledge
* Executing tasks independently or collaboratively

Agents are **stateful**, configurable, and optimized for specialization.

---

## Agent Anatomy

Every agent is defined by three **core identity fields**:

| Field       | Purpose                                       |
| ----------- | --------------------------------------------- |
| `role`      | Who the agent is (job title / responsibility) |
| `goal`      | What the agent is trying to achieve           |
| `backstory` | Context that shapes behavior and tone         |

These three fields act as the **system prompt backbone**.

---

## Core Agent Configuration

```python
Agent(
    role="Research Analyst",
    goal="Find and summarize information",
    backstory="Experienced domain researcher",
    verbose=True,
    memory=False,
    reasoning=False,
    tools=[],
)
```

---

## Common Agent Patterns

### Research Agent

```python
Agent(
    role="Research Analyst",
    goal="Find and summarize information",
    tools=[SerperDevTool()],
    verbose=True
)
```

### Developer Agent

```python
Agent(
    role="Senior Python Developer",
    goal="Write and debug Python code",
    allow_code_execution=True,
    code_execution_mode="safe",
    max_execution_time=300
)
```

### Reasoning Agent

```python
Agent(
    role="Strategic Planner",
    goal="Break down complex problems",
    reasoning=True,
    max_reasoning_attempts=3
)
```

### Multimodal Agent

```python
Agent(
    role="Visual Analyst",
    goal="Analyze text and images",
    multimodal=True
)
```

---

## Memory & Context

Agents can retain information across interactions:

```python
Agent(memory=True)
```

### Context Window Management

| Setting                       | Behavior                             |
| ----------------------------- | ------------------------------------ |
| `respect_context_window=True` | Auto-summarizes when limits exceeded |
| `False`                       | Hard-fails to avoid data loss        |

Use **RAG tools** or **knowledge sources** for large corpora.

---

## Agent Tools

Agents can call tools from:

* CrewAI Toolkit
* LangChain tools
* Custom tools

```python
Agent(tools=[SerperDevTool(), WikipediaTools()])
```

Tools can be overridden **per-task**.

---

## Direct Agent Usage

Agents can be used without tasks or crews:

```python
result = agent.kickoff("Explain LLMs")
print(result.raw)
```

Supports:

* Structured output (Pydantic)
* Async execution
* Message history

---

## Tasks

### What Is a Task?

A **Task** is a well-scoped unit of work assigned to an agent.

Tasks define:

* What should be done
* Expected output
* Tools and constraints
* Validation rules

---

## Task Anatomy

| Attribute         | Purpose                 |
| ----------------- | ----------------------- |
| `description`     | What to do              |
| `expected_output` | Success criteria        |
| `agent`           | Who executes            |
| `tools`           | Allowed tools           |
| `context`         | Inputs from other tasks |
| `output_pydantic` | Structured output       |
| `guardrail`       | Validation              |

---

## YAML-Based Tasks (Recommended)

```yaml
research_task:
  description: Research {topic}
  expected_output: 10 bullet points
  agent: researcher
```

YAML improves:

* Maintainability
* Separation of concerns
* Team collaboration

---

## Task Dependencies

```python
Task(context=[task1, task2])
```

Supports:

* Parallel research
* Fan-in aggregation
* Async workflows

---

## Structured Outputs

### Pydantic Output

```python
Task(output_pydantic=MyModel)
```

Benefits:

* Type safety
* Validation
* Easy downstream usage

---

## Guardrails

Guardrails validate outputs before continuation:

```python
def validate(output):
    return (len(output.raw) > 100, "Too short")
```

Supports:

* Retries
* Feedback loops
* Quality enforcement

---

## Async Tasks

```python
Task(async_execution=True)
```

Used for:

* Parallel research
* Long-running operations

---

## Callbacks

```python
Task(callback=my_function)
```

Use cases:

* Logging
* Notifications
* Persistence

---

## Best Practices

### Agents

* One role = one responsibility
* Enable reasoning only when needed
* Prefer tools over large prompts

### Tasks

* Be explicit in `expected_output`
* Use guardrails for quality
* Use structured outputs between tasks

---

## Mental Model

> **Agents think. Tasks constrain. Crews orchestrate. Flows scale.**

This separation is what makes CrewAI production-ready.

---

## Next Steps

* Add Crews (process orchestration)
* Add Flows (state + control)
* Add RAG + Knowledge
* Add testing & observability

🚀 This README is designed to scale from bootcamp to production systems.



## 12. Creating Custom & Async Tools

### Simple Tool

```python
from crewai.tools import tool

@tool("multiply")
def multiply(a: int, b: int) -> int:
    return a * b
```

### Async Tool

```python
@tool("fetch_async")
async def fetch(q: str) -> str:
    await asyncio.sleep(1)
    return q
```

CrewAI handles sync vs async automatically.

---

## 13. Production Best Practices

### Knowledge

* Fix embedding providers
* Version collections
* Monitor storage size

### Tools

* Cache deterministic outputs
* Add guardrails
* Prefer async for I/O

### Testing

* Run `crewai test` in CI
* Track score drift

---

## Final Mental Model

> **Flows orchestrate.**
> **Crews collaborate.**
> **Agents reason.**
> **Knowledge grounds.**
> **Tools act.**
> **Tests validate.**

This is how you build **real AI systems**, not demos.

---

Happy building with CrewAI 🚀


---

## 🔮 What’s Next

* Tool calling deep dives
* Human-in-the-loop flows
* Advanced memory strategies
* Agent evaluation & testing

---

## ⭐ Final Note

CrewAI is not about prompting.

It’s about **building intelligent systems**.

Welcome to the **CrewAI Bootcamp** 🚀
