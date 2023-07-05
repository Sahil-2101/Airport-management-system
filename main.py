import os
import sys
from datetime import datetime
from utils.helpers import clear_screen, print_header
from ui import handle_main_menu, get_menu_handler

def initialize_system() -> None:
    """Initialize the system and create necessary directories."""
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

def main() -> None:
    """Main application entry point."""
    try:
        # Initialize system
        initialize_system()
        
        # Main application loop
        while True:
            clear_screen()
            choice = handle_main_menu()
            
            if choice == '6':  # Exit
                print_header("Thank you for using Airport Management System!")
                print("\nGoodbye!")
                sys.exit(0)
            
            # Get and execute the appropriate menu handler
            handler = get_menu_handler(choice)
            if handler:
                handler()
                input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 