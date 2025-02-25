def print_right(text):
    # Calculate how many leading spaces are needed
    spaces_needed = 40 - len(text)
    
    # If the string is longer than 40 characters, no spaces are needed
    if spaces_needed > 0:
        # Print the text with the leading spaces
        print(" " * spaces_needed + text)
    else:
        # If the text is too long to fit, print it as is
        print(text)

# Example Usage:
print_right("Monty")
print_right("Python's")
print_right("Flying Circus")
