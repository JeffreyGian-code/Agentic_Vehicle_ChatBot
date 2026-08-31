from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import InMemorySaver
from app.tools.search_vehicle import search_vehicles,get_vehicle_details
from app.tools.finance_tool import calculate_emi
import inspect
load_dotenv()

checkpointer = InMemorySaver()

model = ChatOpenRouter(
    model="nvidia/nemotron-3.5-lightning:free",
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[
        search_vehicles,
        get_vehicle_details,
        calculate_emi,
    ],
    system_prompt=(
        "You are a helpful vehicle assistant. "
        "Use the available tools when needed. "
        "Do not invent vehicle information. "
        "When a search tool returns multiple matching "
        "vehicles, include all matching vehicles in "
        "your response. "
        "If required information is missing, ask "
        "the user instead of making assumptions."
    ),
    middleware=[
        ModelCallLimitMiddleware(
            run_limit=2,
            thread_limit=3,
            exit_behavior="error",
        )
    ],
    checkpointer=checkpointer,
)