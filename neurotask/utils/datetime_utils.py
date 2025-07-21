# utils/datetime_utils.py
import re
from dateutil import parser

def extract_date(text: str):
    """
    Extract and parse a date from the given text.
    
    This function searches for common date patterns (e.g. "03/15/2023",
    "2023-03-15", etc.) and returns a corresponding datetime object.
    If no date is detected, the function returns None.
    
    Args:
        text (str): The text to search for date patterns.
    
    Returns:
        datetime.datetime or None: Parsed date or None if no date found.
    """
    # Regular expression to match various date formats like mm/dd/yyyy, dd-mm-yyyy or yyyy-mm-dd.
    date_pattern = re.compile(
        r'(\b(?:\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})\b)|(\b(?:\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})\b)'
    )
    match = date_pattern.search(text)
    if match:
        try:
            date_str = match.group(0)
            return parser.parse(date_str, fuzzy=True)
        except Exception as e:
            print(f"Date parsing error: {e}")
    return None

# Example usage:
if __name__ == "__main__":
    sample_text = "The meeting was held on 03/15/2023 at the conference room."
    extracted_date = extract_date(sample_text)
    if extracted_date:
        print("Extracted date:", extracted_date.strftime("%Y-%m-%d"))
    else:
        print("No date found.")
