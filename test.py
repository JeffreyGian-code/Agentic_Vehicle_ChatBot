from app.agents.agent import agent

import inspect

print(inspect.signature(ModelCallLimitMiddleware))
config = {
    "configurable": {
        "thread_id": "user-125"
    }
}

for update in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "Find me a Honda under 10 lakh and calculate the EMI for the first one at 8.5% for 5 years.",
            }
        ]
    },
    config=config,
    stream_mode="updates",
):
    print(update)