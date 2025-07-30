from gemini_wrapper import GeminiClient

def main():
    # The system instruction defines the bot's role.
    system_prompt = "You are a helpful movie suggestion bot."

    # Initialize the client with your project and the system prompt.
    # Note: We are specifying the location to test a different region.
    client = GeminiClient(
        project_id="movie-picker-466510",
        location="us-east4",
        system_instruction=system_prompt
    )

    # First user message
    user_prompt_1 = "Recommend me a feel-good comedy from the last 5 years."
    print(f"User: {user_prompt_1}\n")
    reply_1 = client.send_message(user_prompt_1)
    print(f"Gemini says: {reply_1}\n")

    # Follow-up question
    user_prompt_2 = "That sounds interesting! Can you recommend another one that is available on Netflix?"
    print(f"User: {user_prompt_2}\n")
    reply_2 = client.send_message(user_prompt_2)
    print(f"Gemini says: {reply_2}\n")


if __name__ == "__main__":
    main()