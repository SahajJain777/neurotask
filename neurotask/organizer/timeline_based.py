# organizer/timeline_based.py
import os
from neurotask.file_manager.mover import move_file
from datetime import datetime

def organize_by_timeline(directory: str):
    """
    Organize files based on their creation date into folders named "Month Year".
    Example: "March 2024", "June 2025".

    Args:
        directory (str): The directory to scan for files.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                # Get creation time and convert to datetime
                creation_time = os.path.getctime(file_path)
                creation_date = datetime.fromtimestamp(creation_time)
                # Format as "Month Year" (e.g., "March 2024")
                folder_name = creation_date.strftime("%B %Y")  # %B = Full month name
                dest_folder = os.path.join(directory, folder_name)
                move_file(file_path, dest_folder)
            except OSError:  # Fallback if creation time is unavailable
                folder_name = "Unknown_Date"
                dest_folder = os.path.join(directory, folder_name)
                move_file(file_path, dest_folder)