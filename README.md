# Setting up

Add a .env file to root of project with OPENAI_API_KEY=

Get the key from https://platform.openai.com/api-keys

To set your default prompt edit **gpt_initiation_prompt.txt**

## Running


run main.py

Each time you input your question/prompt it must end in a new line with EOF. This allows the terminal to handle multiline inputs.

For example: paste in your question and then press enter, then type EOF and then hit enter again.

When the input has been parsed you with see "Input received." in the terminal.

Press enter to close the chat after you are finished.

The 10th oldest chat will be deleted to minimise disk space consumption.