import json


def write_to_file(latest_chat, filename):
    existing_chat = read_chat_history(filename)
    updated_chat = existing_chat + latest_chat
    with open(filename, "w") as file:
        json.dump(updated_chat, file, indent=4)


def read_chat_history(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def read_file(filename, not_found_response):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(not_found_response)
        return False
    except Exception as e:
        return f"An error occurred: {e}"


def set_text_chat_history(question, chat_name):
    file_path = f"chats/{chat_name}_chat_history.json"
    chat_history = read_chat_history(file_path)
    # Add the system message if the history is empty
    if not chat_history:
        system_prompt = read_file("gpt_initiation_prompt.txt","No initiation prompt found.")
        if system_prompt:
            chat_history.append({"role": "system", "content": system_prompt})
            write_to_file(chat_history, file_path)
    # Append the user's question to the chat history
    chat_history.append({"role": "user", "content": question})
    return chat_history
