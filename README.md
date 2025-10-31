# BlogPostGenerator-Langraph
I have created a system that takes a user question, generates an initial draft using an AI model, enriches it with external search results, and optionally revises it based on critiques.

This project demonstrates a modular workflow using schemas, chains, tool execution, and message graphs, making AI responses more structured, informative, and reliable.


Schemas: Ensure consistent structured outputs (AnswerQuestion, ReviseAnswer).
Responder Chain: Generates the first AI draft.
Retriever / Tool Executor: Runs search queries suggested by AI (via TavilySearch) and feeds results back.
Message Graph: Orchestrates AI responses, tool execution, and optional revisions.
Revisor Chain (Optional): Allows the AI to refine or revise its answer based on feedback.


##Working
User Submits Question

Example request to FastAPI:

import requests

response = requests.post("http://127.0.0.1:8000/generate", json={
    "question": "Who is better, Messi or Ronaldo?"
})
print(response.json())


Responder Chain Generates Draft

AI produces a draft answer using responder_chain.invoke([HumanMessage(content=question)]).

Tool Executor Fetches Search Results

The draft may include suggested search keywords.

execute_tools() takes these keywords, runs TavilySearch, and returns results as ToolMessages.

from tools.executor_tool import execute_tools
tool_results = execute_tools(ai_messages)  # ai_messages come from the responder chain


Message Graph Orchestrates Flow

Nodes in the graph handle:

Initial AI draft

Conditional tool execution

Optional retriever/revisor chain

We use a single iteration due to token limits.

from graphs.reflexion_graph import run_pipeline
final_state = run_pipeline("Who is better, Messi or Ronaldo?")
print(final_state)


Optional Revision

The AI can revise its answer using the revisor_chain based on a critique or missing info:

from chains.revisor_chain import run_revisor
revised_output = run_revisor(previous_answer=final_state, critique={"missing": "more on playing style"})


Return Final Structured Answer

Includes:

Draft answer

Optional revision

Search references

Reflection insights

Project Flow Diagram
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

Key Features

Structured AI responses with Pydantic schemas

Integrated TavilySearch for enriched, referenced answers

Modular, graph-based workflow using LangChain

Optional revision chain for improved quality

Single iteration workflow for simplicity and token efficiency

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

POST a question to /generate endpoint:

{
  "question": "What are the benefits of intermittent fasting?"
}


Sample response:

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

Notes

Currently limited to single iteration due to token constraints.

The system is modular — tools, schemas, or AI models can be swapped easily.

Designed for simplicity and easy understanding of AI + search integration.
