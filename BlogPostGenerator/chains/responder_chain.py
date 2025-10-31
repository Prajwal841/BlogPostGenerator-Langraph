from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import HumanMessage
from schema.schema import AnswerQuestion
import datetime
from dotenv import load_dotenv

load_dotenv()

# 1 Prompt Template
actor_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, list 1–3 search queries separately for researching improvements.
""",
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Answer the user's question above using the required format."),
]).partial(time=lambda: datetime.datetime.now().isoformat())

# 2 Partial the template for first responder
first_responder_prompt = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~100 word answer"
)

# 3 Initialize model
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

# 4 Bind schema as tool
responder_chain = first_responder_prompt | llm.bind_tools(
    tools=[AnswerQuestion],
    tool_choice="AnswerQuestion"
)

# Optional validator
validator = PydanticToolsParser(tools=[AnswerQuestion])
