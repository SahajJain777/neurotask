import os
from neurotask.file_manager.mover import move_file
from neurotask.models.ollama_runner import run_llm

def create_folder_if_not_exists(directory, folder_name):
    """
    Creates a folder if it does not already exist.

    Args:
        directory (str): The parent directory.
        folder_name (str): The name of the folder to create.

    Returns:
        str: The path to the created (or existing) folder.
    """
    folder_path = os.path.join(directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_existing_categories(directory):
    """
    Gets a list of existing subdirectories (potential categories) in the given directory.

    Args:
        directory (str): The directory to check.

    Returns:
        list: A list of folder names (strings).
    """
    return [
        d for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]

def organize_by_semantics(directory: str):
    """
    Organizes files in a directory based on the semantic meaning of their filenames,
    using an LLM to group similar files together. Creates folders for groups of
    related files.

    Args:
        directory (str): The directory to organize.
    """
    try:
        # Get all files (excluding directories)
        filenames = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if not filenames:
            print("[Info] No files found to organize.")
            return

        print(f"[Semantic Organizer] Found {len(filenames)} files to organize")

        # Prepare the prompt for LLM
        prompt = (
            "You are a file organization assistant. Your task is to group similar files together "
            "based solely on their filenames. Analyze the following list of filenames and "
            "group them into logical categories.\n\n"
            "Instructions:\n"
            "1. Identify groups of files that clearly belong together based on their names\n"
            "2. For each group, provide a short, descriptive folder name (2-3 words max)\n"
            "3. If a file doesn't fit any group, mark it as (root) and it will be placed in a Miscellaneous folder\n"
            "4. Use simple, clear category names based on file name patterns\n"
            "5. For similar files (like screenshots), use the common part of the name as category\n"
            "6. IMPORTANT: DO NOT use generic names like 'Category 1', 'Category 2', etc. Always use descriptive names based on content\n\n"
            "Examples of good categorization:\n"
            "invoice_march.pdf -> Invoices\n"
            "invoice_april.pdf -> Invoices\n"
            "screenshot_profile_2024.png -> Profile Screenshots\n"
            "screenshot_profile_2023.png -> Profile Screenshots\n"
            "resume_v2.docx -> Resume Documents\n"
            "random_file.txt -> (root)\n\n"
            "Output format should be:\n"
            "filename1.jpg -> RelevantCategoryName\n"
            "filename2.png -> RelevantCategoryName\n"
            "document.pdf -> AnotherCategory\n"
            "unique_file.txt -> (root)\n\n"
            "Here are the filenames to categorize:\n"
            f"{', '.join(filenames)}\n\n"
            "Now provide your categorization in the specified format. Remember to use meaningful category names based on the file content, never use generic labels like 'Category 1':"
        )

        try:
            # Get the categorization from LLM
            categorization = run_llm(prompt).strip()
            if not categorization:
                print("[Error] LLM did not return any categorization. Please check if Ollama is running with Gemma 3 model.")
                return
                
            print("[LLM Response] Received categorization:")
            print(categorization)
            
            # Process the LLM's response
            category_mapping = {}
            uncategorized_files = []
            for line in categorization.split('\n'):
                if '->' in line:
                    filename_part, category_part = line.split('->', 1)
                    filename = filename_part.strip()
                    category = category_part.strip()
                    
                    if filename in filenames:
                        if category == "(root)" or not category.strip():
                            uncategorized_files.append(filename)
                        else:
                            category_mapping[filename] = category.strip()

            # Organize files based on the mapping
            for filename, category in category_mapping.items():
                dest_folder = create_folder_if_not_exists(directory, category)
                
                # Handle filename conflicts
                base, ext = os.path.splitext(filename)
                counter = 1
                dest_filename = filename
                dest_path = os.path.join(dest_folder, dest_filename)
                while os.path.exists(dest_path):
                    dest_filename = f"{base}_{counter}{ext}"
                    dest_path = os.path.join(dest_folder, dest_filename)
                    counter += 1

                try:
                    move_file(os.path.join(directory, filename), dest_folder, dest_filename)
                    print(f"[Moved] {filename} → {dest_folder}/{dest_filename}")
                except Exception as e:
                    print(f"[Error] Could not move {filename}: {e}")
            
            # Move uncategorized files to Miscellaneous folder
            if uncategorized_files:
                misc_folder = create_folder_if_not_exists(directory, "Miscellaneous")
                print(f"[Info] Moving {len(uncategorized_files)} uncategorized files to Miscellaneous folder")
                
                for filename in uncategorized_files:
                    # Handle filename conflicts
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    dest_filename = filename
                    dest_path = os.path.join(misc_folder, dest_filename)
                    while os.path.exists(dest_path):
                        dest_filename = f"{base}_{counter}{ext}"
                        dest_path = os.path.join(misc_folder, dest_filename)
                        counter += 1
                    
                    try:
                        move_file(os.path.join(directory, filename), misc_folder, dest_filename)
                        print(f"[Moved] {filename} → {misc_folder}/{dest_filename}")
                    except Exception as e:
                        print(f"[Error] Could not move uncategorized file {filename}: {e}")

        except Exception as e:
            print(f"[Error] Failed to process categorization: {e}")
            print("Please ensure Ollama is installed and running with the Gemma 3 model.")
            print("Installation instructions:")
            print("1. Install Ollama from https://ollama.ai")
            print("2. Run: ollama pull gemma3:4b")
            print("3. Start Ollama service")

    except Exception as e:
        print(f"[Error] Failed to organize files: {e}")

if __name__ == "__main__":
    test_directory = "/path/to/your/files"  # Replace with your actual directory path
    organize_by_semantics(test_directory)