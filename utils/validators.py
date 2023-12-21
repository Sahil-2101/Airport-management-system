from typing import Any, Callable

def get_valid_input(prompt: str, expected_type: type, validator: Callable[[Any], bool] = None) -> Any:
    """
    Get valid input from user with type checking and optional validation.
    
    Args:
        prompt: The input prompt to display
        expected_type: The expected type of input (e.g., str, int, float)
        validator: Optional function to validate the input value
        
    Returns:
        The validated input value of the expected type
    """
    while True:
        try:
            value = input(prompt)
            converted_value = expected_type(value)
            
            if validator and not validator(converted_value):
                print(f"Invalid input. Please try again.")
                continue
                
            return converted_value
            
        except ValueError:
            print(f"Invalid input. Expected {expected_type.__name__}.")
        except Exception as e:
            print(f"Error: {str(e)}") 