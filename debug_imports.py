#!/usr/bin/env python
# debug_imports.py - For debugging module import issues

import os
import sys
import importlib
import traceback

def check_import(module_name):
    """Try to import a module and print detailed debug info."""
    print(f"\n----- Checking import for: {module_name} -----")
    try:
        module = importlib.import_module(module_name)
        print(f"✅ Successfully imported {module_name}")
        print(f"Module location: {module.__file__}")
        return module
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"❗ Unexpected error importing {module_name}: {e}")
        traceback.print_exc()
        return None

def check_file_existence(path):
    """Check if a file exists and print debug info."""
    if os.path.exists(path):
        print(f"✅ File exists: {path}")
        if os.path.isdir(path):
            print(f"📁 It's a directory")
        else:
            print(f"📄 It's a file ({os.path.getsize(path)} bytes)")
    else:
        print(f"❌ File doesn't exist: {path}")

def main():
    # Add the project root to the path
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"Project root: {project_root}")
    sys.path.insert(0, project_root)
    
    # Print Python environment info
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print("\nPython path:")
    for p in sys.path:
        print(f"  - {p}")
    
    # Check basic module imports
    check_import("os")
    check_import("shutil")
    
    # Check project modules
    check_import("neurotask.file_manager.mover")
    check_import("neurotask.models.ollama_runner")
    check_import("neurotask.organizer.semantic_based")
    check_import("neurotask.organizer.extension_based")
    
    # Try importing with both styles
    print("\n----- Trying alternate import styles -----")
    try:
        # Try direct import
        print("Trying direct import...")
        from neurotask.file_manager.mover import move_file as move_file1
        print("✅ Direct import successful!")
    except ImportError as e:
        print(f"❌ Direct import failed: {e}")
    
    try:
        # Add neurotask to path and try without prefix
        print("\nTrying import after adding neurotask to path...")
        sys.path.insert(0, os.path.join(project_root, "neurotask"))
        print(f"Updated Python path: {sys.path[0]}")
        from file_manager.mover import move_file as move_file2
        print("✅ Path-based import successful!")
    except ImportError as e:
        print(f"❌ Path-based import failed: {e}")

    # Try running the move_file function with a test file
    print("\n----- Testing move_file function -----")
    try:
        # Create a test file
        test_file = os.path.join(project_root, "test_file.txt")
        test_dir = os.path.join(project_root, "test_output")
        
        with open(test_file, "w") as f:
            f.write("Test content for file moving")
        
        check_file_existence(test_file)
        check_file_existence(test_dir)
        
        # Import and run move_file
        print(f"Attempting to move {test_file} to {test_dir}")
        result = move_file2(test_file, test_dir)
        print(f"move_file result: {result}")
        
        # Check results
        check_file_existence(test_file)
        check_file_existence(test_dir)
        check_file_existence(os.path.join(test_dir, "test_file.txt"))
    except Exception as e:
        print(f"❗ Error testing move_file: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 