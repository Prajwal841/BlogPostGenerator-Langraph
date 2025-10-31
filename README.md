# **BlogPostGenerator-Langraph**

**BlogPostGenerator-Langraph** is a system that takes a user question, generates an initial draft using an AI model, enriches it with external search results, and optionally revises it based on critiques.  

This project demonstrates a **modular workflow** using **schemas, chains, tool execution, and message graphs**, making AI responses more structured, informative, and reliable.

---

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
