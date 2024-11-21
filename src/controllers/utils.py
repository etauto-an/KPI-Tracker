import os


def clear_screen():
    # Check if the OS is Windows or Unix/Linux/Mac and clear screen accordingly
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix/Linux/Mac
        os.system("clear")


def get_nonempty_input(prompt):
    """
    Prompts the user for input and ensures the input is not empty.

    Args:
        prompt (str): The input prompt to display.

    Returns:
        str: The valid, nonempty input provided by the user.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: All fields are required. Please enter valid data.")


def get_numeric_input(prompt, length=4):
    """
    Prompts the user for numeric input and ensures it contains only digits and has the required length.

    Args:
        prompt (str): The input prompt to display.
        length (int, optional): The required length of the input. Defaults to None.

    Returns:
        str: A valid numeric input.
    """
    while True:
        value = input(prompt).strip()
        if value.isdigit():  # Ensures input is numeric and nonempty
            if length and len(value) != length:
                print(
                    f"Error: Input must be exactly {length} digits. Please try again."
                )
            else:
                return value  # Valid numeric input with the correct length
        else:
            print(
                "Error: Input must be numeric and not empty. Please try again."
            )

def hash_pin(pin):
    """
    Hashes a user's PIN for secure storage and comparison.

    Args:
        pin (str): Plain text PIN to hash.

    Returns:
        str: SHA-256 hash of the PIN.
    """
    import hashlib

    return hashlib.sha256(pin.encode()).hexdigest()
