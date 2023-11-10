from dotenv import load_dotenv
from openai import OpenAI
import saftey
import read_write
import talk_to_gpt
import iht_logic
import sys
import boto3

def get_user_id():
    return "1"


def save_progress(user_id, latest_conversation):
    read_write.write_to_file(latest_conversation,f"{user_id}_conversation_history.json")
    step = iht_logic.get_next_user_step(user_id)
    read_write.set_user_step(user_id, step)
    return step


def generate_question(step):
    required_input, non_formatted_question = read_write.get_questions(step)
    user_input = input(required_input)
    sanitized_user_input = saftey.sanitize_string(user_input)
    secret_response = saftey.generate_random_string()
    question = non_formatted_question.format(sanitized_user_input=sanitized_user_input, secret_response=secret_response)
    return question, secret_response


def conversation(client, step=0):
    user_id = get_user_id()

    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    # Reference your table
    table = dynamodb.Table('user_id_to_step')

    step_get_response = table.get_item(
        Key={
            'user_id': f'{user_id}'
        }
    )
    step = step_get_response.get('Item', {}).get('step', None)

    # add error handling here eg not found or non 2XX error

    print(step)

    # step = read_write.get_user_step(user_id)

    question, secret_response = generate_question(step)

    latest_conversation, response_content = talk_to_gpt.text_chat(question, client, user_id)
    if response_content == secret_response:
        conversation(client, step)

    if save_progress(user_id, latest_conversation) == 1:
        print("You have completed your form, please take your time to review it. Best Wishes.")
        sys.exit()


def start_up():
    load_dotenv()
    client = OpenAI()
    conversation(client)


if __name__ == '__main__':
    read_write.set_user_step(get_user_id(), 0) # remove this, just keeping it here because I don't have steps past 0, so it must keep returning there
    start_up()
