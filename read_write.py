import json
import os


def write_to_file(latest_conversation, filename):
    existing_conversation = read_conversation_history(filename)
    updated_conversation = existing_conversation + latest_conversation
    with open(filename, "w") as file:
        json.dump(updated_conversation, file, indent=4)


def read_conversation_history(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def delete_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        # Silently handle the case where the file does not exist
        pass
    except Exception as e:
        print(f"An error occurred: {e}")


def read_file(filename, not_found_response):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(not_found_response)
        return False
    except Exception as e:
        return f"An error occurred: {e}"


def set_text_conversation_history(question, chat_name):
    file_path = f"{chat_name}_conversation_history.json"
    conversation_history = read_conversation_history(file_path)
    # Add the system message if the history is empty
    if not conversation_history:
        system_prompt = read_file("gpt_initiation_prompt.txt","No initiation prompt found.")
        if system_prompt:
            conversation_history.append({"role": "system", "content": system_prompt})
            read_conversation_history(file_path)
            write_to_file(conversation_history, f"{chat_name}_chat_history.json")
    # Append the user's question to the conversation history
    conversation_history.append({"role": "user", "content": question})
    return conversation_history
