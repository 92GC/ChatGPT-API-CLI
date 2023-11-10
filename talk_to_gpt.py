import read_write


def text_chat(question, client, user_id, set_up_prompt=None, model=None):
    # Read the existing conversation history
    conversation_history = read_write.read_conversation_history(f"{user_id}_conversation_history.json")

    # Add the system message if the history is empty
    if not conversation_history:
        conversation_history.append({"role": "system", "content": "You are a name parser when extract and return the name from a message you are sent."})

    # Append the user's question to the conversation history
    conversation_history.append({"role": "user", "content": question})

    # Get the response from GPT
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=conversation_history
    )

    # Extract the content of the response
    response_content = response.choices[0].message.content

    # Print the response content
    print("Response:", response_content)

    # Prepare the new conversation to be written to the file
    latest_conversation = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": response_content}
    ]

    return latest_conversation, response_content
