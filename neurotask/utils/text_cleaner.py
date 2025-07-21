# utils/text_cleaner.py
import re

def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace and non-ASCII characters.
    
    Args:
        text (str): The text to clean.
    
    Returns:
        str: Cleaned text.
    """
    # Remove leading/trailing spaces.
    text = text.strip()
    # Replace multiple whitespace characters (spaces, newlines, etc.) with a single space.
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters.
    text = text.encode('ascii', errors='ignore').decode()
    return text

# Example usage:
if __name__ == "__main__":
    dirty_text = "  This is   a sample text.\nIt contains \tsome\tirregular formatting—and non-ASCII: café.   "
    print("Cleaned text:", clean_text(dirty_text))
