import json
from graphs.reflexion_graph import run_pipeline
from schema.schema import AnswerQuestion, ReviseAnswer
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

if __name__ == "__main__":
    user_question = "Explain how AI tools are change content creationin2025."

    # Run the reflexion pipeline
    final_state = run_pipeline(user_question)

    # Print all intermediate messages
    print("\n📝 Full conversation state:\n")
    messages = final_state["messages"]

    for idx, msg in enumerate(messages, start=1):
        print(f"Message {idx}: {msg.__class__.__name__}")

        # HumanMessage: direct content
        if isinstance(msg, HumanMessage):
            print(msg.content)

        # AIMessage: check for content or tool_calls
        elif isinstance(msg, AIMessage):
            if msg.content:
                print(msg.content)
            if getattr(msg, "tool_calls", None):
                for call_idx, call in enumerate(msg.tool_calls, start=1):
                    print(f"  Tool Call {call_idx}:")
                    print(json.dumps(call.get("args", {}), indent=2))

        # ToolMessage: usually structured output
        elif isinstance(msg, ToolMessage):
            if msg.content:
                try:
                    parsed = json.loads(msg.content)
                    print(json.dumps(parsed, indent=2))
                except:
                    print(msg.content)
        else:
            print("<No displayable content>")

        print("-" * 50)

    # Print final validated response (if any)
    final_msg = messages[-1]
    validated = None

    if getattr(final_msg, "tool_calls", None):
        tool_args = final_msg.tool_calls[0]["args"]
        tool_name = final_msg.tool_calls[0]["name"]
        if tool_name == "ReviseAnswer":
            validated = ReviseAnswer(**tool_args)
        elif tool_name == "AnswerQuestion":
            validated = AnswerQuestion(**tool_args)

    if validated:
        print("\n✅ Final Validated Response (Parsed JSON):\n")
        print(validated.model_dump_json(indent=2))
