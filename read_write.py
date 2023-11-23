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


def delete_conversation_history(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        # Silently handle the case where the file does not exist
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
