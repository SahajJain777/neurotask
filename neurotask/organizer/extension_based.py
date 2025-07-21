import os
import platform
from neurotask.file_manager.mover import move_file
from typing import Dict

def organize_by_extension(directory: str, extension_map: Dict[str, list]):
    """
    Organize files in the given directory based on their file extension.
    After organization, opens the target directory in the system file explorer.

    Args:
        directory (str): The directory to scan for files.
        extension_map (dict): A mapping of category names to file extensions.
    """
    # First organize all files
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            target_category = None
            for category, extensions in extension_map.items():
                if ext in extensions:
                    target_category = category.capitalize()
                    break
            if target_category:
                dest_folder = os.path.join(directory, target_category)
                move_file(file_path, dest_folder)
    
    # After organization completes, open the directory
    open_directory_in_explorer(directory)

def open_directory_in_explorer(path: str):
    """
    Open the specified directory in the system file explorer.
    
    Args:
        path (str): Path to the directory to open.
    """
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{path}"')
        else:  # Linux and other Unix-like systems
            os.system(f'xdg-open "{path}"')
    except Exception as e:
        print(f"Error opening directory: {e}")