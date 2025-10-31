from pydantic import BaseModel, Field
from typing import List
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage

class Reflection(BaseModel):
    missing: str = Field(..., description="What is missing from the current answer?")
    superfluous: str = Field(..., description="What is superfluous in the current answer?")

class AnswerQuestion(BaseModel):
    answer: str = Field(..., description="The answer to the user's question.")
    references: List[str] = Field(..., description="List of references used in the answer.")
    reflection: Reflection = Field(..., description="Critical reflection on the answer.")
    search_queries: List[str] = Field(..., description="List of search queries to verify the answer.")

class ReviseAnswer(BaseModel):
    answer: str = Field(..., description="The revised and improved answer to the user's question.")
    references: List[str] = Field(..., description="List of references used in the revised answer.")
    reflection: Reflection = Field(..., description="Critical reflection on the previous answer.")
    search_queries: List[str] = Field(..., description="List of search queries to verify the revised answer.")

# Input schema
class QuestionRequest(BaseModel):
    question: str

# Output schema
class PipelineResponse(BaseModel):
    final_output: dict
    conversation: list

class GraphState(Dict[str, Any]):
    messages: List[BaseMessage]