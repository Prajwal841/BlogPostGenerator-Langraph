from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from schema.schema import ReviseAnswer
from chains.responder_chain import actor_prompt_template
from copy import deepcopy
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

# Revision instructions
revise_instructions = """Revise your previous answer using the critique provided.
- Add missing insights and correct weak reasoning.
- Remove unnecessary or repetitive information.
- The revised answer should be ~10 words.
- Include 1–3 credible sources as numerical citations like [1], [2].
- At the end, append a 'References' section in this format:
  [1] https://example.com
  [2] https://another-source.com
"""

# Prepare prompt
revisor_prompt = deepcopy(actor_prompt_template)
revisor_prompt.messages = revisor_prompt.messages[:-1]
revisor_prompt = revisor_prompt.partial(first_instruction=revise_instructions)

# Bind LLM to ReviseAnswer
revisor_chain = llm.bind_tools(
    tools=[ReviseAnswer],
    tool_choice="ReviseAnswer"
)

# Optional parser/validator
validator = PydanticToolsParser(tools=[ReviseAnswer])

# Function to invoke safely
def run_revisor(previous_answer: dict, critique: dict):
    tool_input = {
        "answer": previous_answer["answer"],
        "references": previous_answer.get("references", []),
        "reflection": critique,
        "search_queries": previous_answer.get("search_queries", [])
    }
    message = HumanMessage(content=tool_input)
    revised_output = revisor_chain.invoke([message])
    return validator.parse(revised_output)
