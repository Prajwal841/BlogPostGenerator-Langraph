# **BlogPostGenerator-Langraph**

**BlogPostGenerator-Langraph** is a system that takes a user question, generates an initial draft using an AI model, enriches it with external search results, and optionally revises it based on critiques.  

This project demonstrates a **modular workflow** using **schemas, chains, tool execution, and message graphs**, making AI responses more structured, informative, and reliable.

<img width="1757" height="785" alt="image" src="https://github.com/user-attachments/assets/c6ccfe9f-15d3-4d91-a430-53f42ccf6219" />

---
<img width="1872" height="867" alt="image" src="https://github.com/user-attachments/assets/657088dc-7623-4a59-9c6a-21d0f33e32b3" />

## **Key Components**

- **Schemas:** Ensure consistent structured outputs (`AnswerQuestion`, `ReviseAnswer`).  
- **Responder Chain:** Generates the first AI draft.  
- **Retriever / Tool Executor:** Runs search queries suggested by AI (via **TavilySearch**) and feeds results back.  
- **Message Graph:** Orchestrates AI responses, tool execution, and optional revisions.  
- **Revisor Chain (Optional):** Allows the AI to refine or revise its answer based on feedback.  

---

## **Workflow**

### **1. User Submits Question**

Example request to FastAPI:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/generate", 
    json={"question": "Who is better, Messi or Ronaldo?"}
)
print(response.json())

```
## 2. Responder Chain Generates Draft

AI produces a draft answer using:

```python
from langchain_core.messages import HumanMessage

draft = responder_chain.invoke([HumanMessage(content=question)])
```
## 3. Tool Executor Fetches Search Results

execute_tools() takes these keywords, runs TavilySearch, and returns results as ToolMessages:
```python

from tools.executor_tool import execute_tools
tool_results = execute_tools(ai_messages)  # ai_messages come from the responder chain

```
Note: For each keyword, TavilySearch returns up to 2 results by default.

## 4. Message Graph Orchestrates Flow

Nodes in the graph handle:
Initial AI draft
Conditional tool execution
Optional retriever/revisor chain

We use a single iteration due to token limits.
```python

from graphs.reflexion_graph import run_pipeline

final_state = run_pipeline("Who is better, Messi or Ronaldo?")
print(final_state)
```
## 5. Optional Revision

The AI can revise its answer using the revisor_chain based on a critique or missing info:
```python

from chains.revisor_chain import run_revisor

revised_output = run_revisor(
    previous_answer=final_state, 
    critique={"missing": "more on playing style"}
)
```
## 6. Return Final Structured Answer

The final output includes:

Draft answer
Optional revision
Search references
Reflection insights

## Project Flow Diagram
User Question
      │
      ▼
Responder Chain ──► AI Draft ──┐
                              ▼
                     Tool Executor (TavilySearch)
                              │
                              ▼
                      Updated AI Draft
                              │
                              ▼
                       Revisor Chain (Optional)
                              │
                              ▼
                      Final Structured Answer

### Key Features
Structured AI responses with Pydantic schemas
Integrated TavilySearch for enriched, referenced answers
Modular, graph-based workflow using LangChain
Optional revision chain for improved quality
Single iteration workflow for simplicity and token efficiency

### File Structure & Key Modules
BlogPostGenerator/
│
├── app.py                  # FastAPI main entry point
├── graphs/
│   └── reflexion_graph.py  # Orchestrates AI draft, tool calls, optional revisions
├── chains/
│   ├── responder_chain.py  # Generates initial AI draft
│   └── revisor_chain.py    # Optional refinement of AI answers
├── tools/
│   └── executor_tool.py    # Executes search queries (TavilySearch)
├── schema/
│   └── schema.py           # Pydantic schemas for structured output
└── requirements.txt        # Dependencies

Installation
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app:app --reload

Usage Example
```python

POST a question to /generate endpoint:

{
  "question": "What are the benefits of intermittent fasting?"
}

```

Sample response:
```python

{
  "answer": "Intermittent fasting improves metabolism, reduces belly fat, and supports mental clarity.",
  "references": [
    "https://www.healthline.com/nutrition/intermittent-fasting-guide",
    "https://www.medicalnewstoday.com/articles/intermittent-fasting"
  ],
  "reflection": {
    "missing": "More scientific studies could be cited",
    "superfluous": "Extra details on diet types"
  }
}
```
Notes

Currently limited to single iteration due to token constraints.

The system is modular — tools, schemas, or AI models can be swapped easily.
