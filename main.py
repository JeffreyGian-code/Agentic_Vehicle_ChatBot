from app.agents.agent import agent


config = {
    "configurable": {
        "thread_id": "user-123"
    }
}


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        },
        config=config,
    )

    print("AI:", result["messages"][-1].content)