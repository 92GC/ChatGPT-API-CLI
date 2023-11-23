from dotenv import load_dotenv
from openai import OpenAI
import read_write
import api
import sys


def get_chat_name():
    return "1"


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


def new_chat_or_not():
    new_chat = get_yes_or_no("Do you want to start a new chat? (y/n): ")
    if new_chat:
        read_write.delete_conversation_history(f"{get_chat_name()}_chat_history.json")


def conversation(client):
    chat_name = get_chat_name()
    question = generate_question()
    latest_conversation, response_content = api.text_chat(question, client, chat_name)
    read_write.write_to_file(latest_conversation, f"{chat_name}_chat_history.json")
    conversation(client)


def start_up():
    load_dotenv()
    client = OpenAI()
    new_chat_or_not()

    conversation(client)


if __name__ == '__main__':
    start_up()
