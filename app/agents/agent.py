from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import InMemorySaver
from app.tools.search_vehicle import search_vehicles,get_vehicle_details

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
    ],
    system_prompt=(
        "You are a helpful vehicle assistant. "
        "Use the available tools when needed. "
        "Do not invent vehicle information."
    ),
    checkpointer=checkpointer,
)
