def make_text_request(chat_history, question, client, set_up_prompt=None, model=None):

    # Get the response from GPT
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=chat_history
    )

    # Extract the content of the response
    response_content = response.choices[0].message.content

    # Print the response content
    print("Response:", response_content)

    # Prepare the new chat to be written to the file
    latest_chat = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": response_content}
    ]

    return latest_chat
