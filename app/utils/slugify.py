import re

def to_slug(s: str) -> str:
    """
    Convert a given string into a slug.
    
    Args:
        s (str): The input string to be converted to a slug.
        
    Returns:
        str: The slugified version of the input string.
    
    Raises:
        ValueError: If the input string is empty.
    """
    
    if not s:
        raise ValueError("The input string cannot be empty.")
    
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s
