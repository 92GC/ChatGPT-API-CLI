from dotenv import load_dotenv
from openai import OpenAI
import read_write
import api_calls
import sys
from datetime import datetime
import os


chat_timestamp = None


def set_chat_name(previous=None):
    global chat_timestamp
    if not previous:
        chat_timestamp = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    else:
        chat_timestamp = previous
    return chat_timestamp


def get_chat_name():
    global chat_timestamp
    return chat_timestamp


def get_multiline_input(sentinel='EOF'):
    print(f"Enter/paste your text. Type '{sentinel}' on a new line when done:")
    lines = []
    while True:
        try:
            line = input()
            if not lines and line == "":
                return ""
            if line.strip() == sentinel:
                break
            lines.append(line)
        except EOFError:  # Handle Ctrl-D (EOF) gracefully
            break

    print("Input received.")
    return '\n'.join(lines)


def generate_question():

    user_input = get_multiline_input(sentinel='EOF')
    if user_input == "":
        print("Exiting chat.")
        sys.exit(0)
    return user_input


def get_yes_or_no(prompt):
    while True:
        response = input(prompt).lower()
        if response in ['yes', 'y', 'Y', '']:
            return True
        elif response in ['no', 'n', 'N']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")


def delete_older_chats(directory):
    all_files = os.listdir(directory)
    chat_files = [file for file in all_files if file.endswith('_chat_history.json')]
    chat_files.sort(key=lambda x: datetime.strptime(x, "%H-%M-%S_%d-%m-%Y_chat_history.json"), reverse=True)
    for file in chat_files[9:]:
        os.remove(os.path.join(directory, file))


def find_most_recent_timestamp(directory):
    all_files = os.listdir(directory)
    timestamps = [datetime.strptime(file.split('_chat_history')[0], '%H-%M-%S_%d-%m-%Y')
                  for file in all_files if file.endswith('_chat_history.json') and '_' in file]
    max_time = max(timestamps, default=None)

    return max_time.strftime('%H-%M-%S_%d-%m-%Y') if max_time else None
# todo Refactor to return ordered list

def handle_new_chat():
    start_new_chat = get_yes_or_no("Do you want to start a new chat? (y/n): ")
    if start_new_chat:
        delete_older_chats("chats/")
        set_chat_name()
    else:
        most_recent_timestamp = find_most_recent_timestamp("chats/")
        if most_recent_timestamp:
            # todo Refactor to display and require numbered user input for chat
            set_chat_name(previous=most_recent_timestamp)
        else:
            print("No existing chats to load.")
            set_chat_name()


def conversation(client):
    chat_name = get_chat_name()
    question = generate_question()

    conversation_history = read_write.set_text_conversation_history(question, chat_name)
    latest_conversation = api_calls.make_text_request(conversation_history, question, client)
    read_write.write_to_file(latest_conversation, f"chats/{chat_name}_chat_history.json")

    conversation(client)


def start_up():
    load_dotenv()
    client = OpenAI()
    handle_new_chat()
    conversation(client)


if __name__ == '__main__':
    start_up()
