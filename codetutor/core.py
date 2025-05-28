def print_tutor_response(text: str):
    """Nicely format tutor responses with green text in the terminal."""
    print(f"\033[0m\nTutor: \033[92m{text}\n\033[0m")


def print_error(message: str):
    """Print errors in red."""
    print(f"\033[91m❌ {message}\033[0m")


def print_info(message: str):
    """Print info in cyan."""
    print(f"\033[96mℹ️ {message}\033[0m")
