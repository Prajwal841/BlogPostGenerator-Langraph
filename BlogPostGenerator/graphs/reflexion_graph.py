from typing import List, Dict, Any
import json
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from chains.responder_chain import responder_chain
from chains.revisor_chain import revisor_chain
from tools.executor_tool import execute_tools
from schema.schema import AnswerQuestion, ReviseAnswer, GraphState

MAX_ITERATIONS = 2



def draft_node(state: GraphState) -> GraphState:
    messages = state["messages"]
    response = responder_chain.invoke(messages)
    return {"messages": messages + [response]}

def execute_tools_node(state: GraphState) -> GraphState:
    messages = state["messages"]
    tool_results = execute_tools(messages)
    return {"messages": messages + tool_results}

def revisor_node(state: GraphState) -> GraphState:
    messages = state["messages"]
    revision = revisor_chain.invoke(messages)
    return {"messages": messages + [revision]}

def loop_condition(state: GraphState):
    messages = state["messages"]
    tool_calls_count = sum(isinstance(msg, ToolMessage) for msg in messages)
    if tool_calls_count >= MAX_ITERATIONS:
        return END
    return "execute_tools"

# Graph setup
graph_builder = StateGraph(GraphState)
graph_builder.add_node("draft", draft_node)
graph_builder.add_node("execute_tools", execute_tools_node)
graph_builder.add_node("revisor", revisor_node)
graph_builder.set_entry_point("draft")
graph_builder.add_edge("draft", "execute_tools")
graph_builder.add_edge("execute_tools", "revisor")
graph_builder.add_conditional_edges("revisor", loop_condition)
graph = graph_builder.compile()

def run_pipeline(user_input: str):
    user_message = HumanMessage(content=user_input)
    initial_state = {"messages": [user_message]}
    final_state = graph.invoke(initial_state)
    
    messages = final_state["messages"]

    print("\n📝 Full conversation state:\n")
    for idx, msg in enumerate(messages, start=1):
        msg_type = msg.__class__.__name__
        print(f"Message {idx}: {msg_type}")
        # ToolMessage might have JSON content
        if isinstance(msg, ToolMessage):
            try:
                content = json.dumps(json.loads(msg.content), indent=2)
            except:
                content = msg.content
        else:
            content = getattr(msg, "content", msg)
        print(content)
        print("-" * 50)

    # Final validated response if last message was a tool call
    final_msg = messages[-1]
    if hasattr(final_msg, "tool_calls") and final_msg.tool_calls:
        tool_args = final_msg.tool_calls[0]["args"]
        if final_msg.tool_calls[0]["name"] == "ReviseAnswer":
            validated = ReviseAnswer(**tool_args)
        else:
            validated = AnswerQuestion(**tool_args)

        print("\n✅ Final Validated Response (Parsed JSON):\n")
        print(validated.model_dump_json(indent=2))
    else:
        print("\n⚠️ No tool calls found in the final response!")

    return final_state
