# organizer/intent_based.py
import os
from neurotask.file_manager.reader import read_first_page
from neurotask.file_manager.mover import move_file
from neurotask.models.ollama_runner import run_llm

def organize_by_intents(directory: str):
    """
    Organize files by inferring the document's intent or next action.
    Uses the LLM to decide what should be done with the file (e.g., To_Read, To_Sign)
    and moves the file into a corresponding folder.

    Args:
        directory (str): The directory to scan for files.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            content = read_first_page(file_path)
            if not content.strip():
                intent = "Unknown_Intent"
            else:
                prompt = (
                    "You are a document categorization assistant. Your task is to determine the most appropriate "
                    "action category for a document based on its content.\n\n"
                    "Instructions:\n"
                    "1. Analyze the document content carefully\n"
                    "2. Determine what the next logical action should be for this document\n"
                    "3. Choose the most suitable category from: To_Read, To_Sign, To_Review, To_Complete, To_Reply, To_File, Reference\n"
                    "4. If none of these fit, suggest a concise, action-oriented category (2-3 words max)\n"
                    "5. Output only the category name, nothing else\n\n"
                    "Document content:\n"
                    f"{content}\n\n"
                    "Document category:"
                )
                intent = run_llm(prompt)
                # Cleanup intent text for folder naming.
                intent = intent.strip().replace(" ", "_")
            dest_folder = os.path.join(directory, f"Intent_{intent}")
            move_file(file_path, dest_folder)
