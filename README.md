# Setting Up

1. Add a `.env` file to the root of your project with `OPENAI_API_KEY=`.
2. Obtain the key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
3. Even if it says you have free credit you need to buy some credit to gain access.
4. To set your default prompt, edit **gpt_initiation_prompt.txt**.

## Running

1. Run `main.py`.
2. When inputting your question or prompt, ensure it ends with a newline followed by `e`. This facilitates handling multi-line inputs in the terminal.

   For instance: Paste your question, press Enter, type `EOF`, and then press Enter again.

3. Once the input is parsed, "Input received." will appear in the terminal.
4. Press Enter to close the chat when you are finished.
5. To minimize disk space consumption, the 10th oldest chat will be automatically deleted.
