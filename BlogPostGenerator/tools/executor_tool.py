import json
from typing import List, Dict, Any
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_tavily import TavilySearch

# Initialize the Tavily search tool
tavily_tool = TavilySearch(max_results=2)

def execute_tools(messages: List[BaseMessage]) -> List[ToolMessage]:
    """
    Executes search queries from the latest AI tool calls.
    Supports AnswerQuestion, ReviseAnswer, and TavilySearch calls.
    Returns a list of ToolMessage objects containing search results.
    """
    tool_messages: List[ToolMessage] = []

    for msg in messages:
        if not isinstance(msg, AIMessage) or not getattr(msg, "tool_calls", None):
            continue

        for tool_call in msg.tool_calls:
            tool_name = tool_call.get("name")
            call_id = tool_call.get("id")
            args = tool_call.get("args", {})

            # Only handle tools with search_queries
            search_queries = args.get("search_queries", []) or args.get("query", [])
            if not search_queries:
                continue

            query_results: Dict[str, Any] = {}
            for query in search_queries:
                try:
                    result = tavily_tool.invoke(query)
                    query_results[query] = result
                except Exception as e:
                    query_results[query] = {"error": str(e)}

            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results, ensure_ascii=False, indent=2),
                    tool_call_id=call_id
                )
            )

    return tool_messages
