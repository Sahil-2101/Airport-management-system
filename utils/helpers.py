import os
import platform

def clear_screen() -> None:
    """Clear the terminal screen based on the operating system."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_header(text: str) -> None:
    """Print a formatted header with the given text."""
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60 + "\n") 