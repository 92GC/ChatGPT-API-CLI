import read_write
import os


def text_chat(question, client, chat_name, set_up_prompt=None, model=None):
    file_path = f"{chat_name}_conversation_history.json"
    conversation_history = read_write.read_conversation_history(file_path)
    # Add the system message if the history is empty
    if not conversation_history and "CHATGPT_INITIATION_PROMPT" in os.environ:
        system_prompt = os.environ.get("CHATGPT_INITIATION_PROMPT")
        conversation_history.append({"role": "system", "content": system_prompt})

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
