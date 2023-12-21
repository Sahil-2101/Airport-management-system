import os
import platform

def clear_screen() -> None:
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "="*50)
    print(f"{title:^50}")
    print("="*50) 