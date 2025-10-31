from fastapi import FastAPI
from graphs.reflexion_graph import run_pipeline
from schema.schema import QuestionRequest, PipelineResponse

# FastAPI app instance
app = FastAPI(title="Reflexion Graph API", version="1.0")



@app.post("/generate", response_model=PipelineResponse)
def generate_answer(request: QuestionRequest):
    """
    Run the Reflexion Graph pipeline for the given user question.
    Returns the final validated output + all intermediate messages.
    """
    final_state = run_pipeline(request.question)
    messages = final_state["messages"]

    # Extract last validated output if available
    final_msg = messages[-1]
    final_output = {}

    if hasattr(final_msg, "tool_calls") and final_msg.tool_calls:
        tool_args = final_msg.tool_calls[0]["args"]
        final_output = tool_args
    else:
        final_output = {"error": "No valid tool output found."}

    # Convert messages to readable structure for API response
    formatted_messages = []
    for idx, msg in enumerate(messages, start=1):
        formatted_messages.append({
            "index": idx,
            "type": msg.__class__.__name__,
            "content": getattr(msg, "content", ""),
        })

    return {
        "final_output": final_output,
        "conversation": formatted_messages
    }
