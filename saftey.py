import random
import string


def sanitize_string(input_string):
    # Allow only letters, spaces, hyphens, and apostrophes
    sanitized = [char for char in input_string if char.isalpha() or char in [" ", "-", "’"]]

    # Join the list of characters back into a string and strip leading/trailing spaces
    return ''.join(sanitized).strip()


def generate_random_string(length=10):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits  # This includes both letters and numbers

    # Randomly choose 'length' characters and join them into a string
    return ''.join(random.choice(characters) for _ in range(length))
