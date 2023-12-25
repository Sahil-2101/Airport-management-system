from typing import Any, Callable, TypeVar, Optional

T = TypeVar('T')

def get_valid_input(prompt: str, expected_type: type, validator: Optional[Callable[[Any], bool]] = None) -> T:
    """
    Get valid input from the user.
    
    Args:
        prompt: The input prompt to display
        expected_type: The expected type of the input
        validator: Optional validation function that returns True if input is valid
        
    Returns:
        The validated input of the expected type
    """
    while True:
        try:
            user_input = input(prompt)
            converted_input = expected_type(user_input)
            
            if validator and not validator(converted_input):
                print(f"Invalid input. Please try again.")
                continue
                
            return converted_input
            
        except ValueError:
            print(f"Invalid input. Please enter a valid {expected_type.__name__}.")
        except Exception as e:
            print(f"An error occurred: {str(e)}") 