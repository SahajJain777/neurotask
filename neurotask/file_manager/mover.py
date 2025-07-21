# file_manager/mover.py
import os
import shutil

def move_file(source_path: str, dest_folder: str, new_filename: str = None) -> bool:
    """
    Move a file to a destination folder, optionally with a new filename.
    Creates the destination folder if it doesn't exist.
    
    Args:
        source_path (str): Path to the source file
        dest_folder (str): Path to the destination folder
        new_filename (str, optional): New name for the file. If None, keeps original name.
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"[DEBUG] Moving file: {source_path}")
        print(f"[DEBUG] Destination folder: {dest_folder}")
        
        # Check if source file exists
        if not os.path.exists(source_path):
            print(f"[DEBUG] Source file does not exist: {source_path}")
            return False
            
        # Create destination folder if it doesn't exist
        if not os.path.exists(dest_folder):
            print(f"[DEBUG] Creating destination folder: {dest_folder}")
            os.makedirs(dest_folder)
            
        # Get the destination path
        if new_filename is None:
            new_filename = os.path.basename(source_path)
        dest_path = os.path.join(dest_folder, new_filename)
        print(f"[DEBUG] Final destination path: {dest_path}")
        
        # Move the file
        shutil.move(source_path, dest_path)
        print(f"[DEBUG] File successfully moved")
        return True
        
    except Exception as e:
        print(f"[DEBUG] Error details: {str(e)}")
        print(f"Error moving file {source_path}: {str(e)}")
        return False

