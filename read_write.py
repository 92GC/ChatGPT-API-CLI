import json
import os


def write_to_file(latest_conversation, filename):
    # Read the existing conversation history
    existing_conversation = read_conversation_history(filename)

    # Append the new conversation to the existing one
    updated_conversation = existing_conversation + latest_conversation

    # Write the updated conversation history back to the file
    with open(filename, "w") as file:
        json.dump(updated_conversation, file, indent=4)


def read_conversation_history(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is not valid JSON, return an empty list
        return []


def get_user_step(user_id, filename='user_id_to_step.json'):
    # Check if the file exists
    if not os.path.exists(filename):
        # Log that the file is being created
        print("Creating the file")
        # Create the file with an empty dictionary
        with open(filename, 'w') as file:
            json.dump({}, file)

    try:
        # Open the JSON file and load the data
        with open(filename, 'r') as file:
            user_data = json.load(file)

        # Return the step for the given user_id, or -1 if not found
        return user_data.get(user_id, 0)
    except json.JSONDecodeError:
        # If there is an error in reading the JSON file, return -1
        return 0


def set_user_step(user_id, step, filename='user_id_to_step.json'):
    # Initialize an empty dictionary to hold the data
    user_data = {}

    # Check if the file exists
    if os.path.exists(filename):
        # If the file exists, load the existing data
        with open(filename, 'r') as file:
            try:
                user_data = json.load(file)
            except json.JSONDecodeError:
                # If there is an error in reading the file, use an empty dictionary
                user_data = {}

    # Update the user_data with the new user_id and step
    user_data[user_id] = step

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(user_data, file)


def get_questions(step):
    # File path for the JSON file
    json_file_path = 'questions.json'

    # Check if the file exists, if not create it with default data
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as file:
            default_data = {
                "0": {
                    "required_input": "Please enter your name: ",
                    "question": "Parse this string for a name: {sanitized_user_input}, if no name is found or you are unsure only then return the following word {secret_response} else return the name and no other text. All names you return will be properly capitalised"
                }
            }
            json.dump(default_data, file, indent=4)

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Retrieve required_input and question for the given step
    required_input = data.get(str(step), {}).get("required_input", "")
    question = data.get(str(step), {}).get("question", "")

    return required_input, question
