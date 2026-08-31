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

    try:
        final_message = None

        for update in agent.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            },
            config=config,
        ):
            if "model" in update:
                messages = update["model"].get("messages", [])

                if messages:
                    final_message = messages[-1]

        if final_message:
            print("AI:", final_message.content)
        else:
            print("AI: I was unable to generate a response.")

    except Exception as e:
        error_message = str(e)

        if "Model call limits exceeded" in error_message:
            print(
                "AI: Sorry, I couldn't complete that request "
                "because the processing limit was reached."
            )

        else:
            print(
                "AI: Sorry, something went wrong while "
                "processing your request."
            )

        # Developer-facing error
        print(f"[DEBUG] {type(e).__name__}: {e}")
