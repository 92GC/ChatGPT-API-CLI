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
    print(f"Enter/paste your text. Press Cmd+d or type '{sentinel}' on a new line when done:")
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
    user_input = get_multiline_input()
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


def find_most_recent_timestamps(directory):
    all_files = os.listdir(directory)
    timestamps = [datetime.strptime(file.split('_chat_history')[0], '%H-%M-%S_%d-%m-%Y')
                  for file in all_files if file.endswith('_chat_history.json') and '_' in file]

    sorted_timestamps = sorted(timestamps, reverse=True)
    return [time.strftime('%H-%M-%S_%d-%m-%Y') for time in sorted_timestamps]


def select_chat_history(timestamps):
    for i, timestamp in enumerate(timestamps, 1):
        print(f"{i}. {timestamp}")

    while True:
        try:
            choice = int(input("Enter the number of your chat: "))
            if 1 <= choice <= len(timestamps):
                return timestamps[choice - 1]
            else:
                print("Invalid number, please try again.")
        except ValueError:
            print("Please enter a valid number.")


def handle_new_chat():
    start_new_chat = get_yes_or_no("Do you want to start a new chat? (y/n): ")
    if start_new_chat:
        delete_older_chats("chats/")
        set_chat_name()
    else:
        timestamps = find_most_recent_timestamps("chats/")
        if timestamps:
            if len(timestamps) == 1:
                selected_timestamp = timestamps[0]
            else:
                selected_timestamp = select_chat_history(timestamps)
            set_chat_name(previous=selected_timestamp)
        else:
            print("No existing chats to load.")
            set_chat_name()


def chat(client):
    chat_name = get_chat_name()
    question = generate_question()

    chat_history = read_write.set_text_chat_history(question, chat_name)
    latest_chat = api_calls.make_text_request(chat_history, question, client)
    read_write.write_to_file(latest_chat, f"chats/{chat_name}_chat_history.json")

    chat(client)


def start_up():
    load_dotenv()
    client = OpenAI()
    handle_new_chat()
    chat(client)


if __name__ == '__main__':
    start_up()
