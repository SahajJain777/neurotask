#!/usr/bin/env python3
"""
Neurotask main entry point - handles CLI, GUI, or Web interface launching
"""
import os
import sys
import argparse

def main():
    """Main entry point for the application"""
    # Add the parent directory to the system path to enable imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    parser = argparse.ArgumentParser(description='Neurotask File Organizer')
    parser.add_argument('--cli', action='store_true', help='Run in command line mode')
    parser.add_argument('--gui', action='store_true', help='Run with graphical user interface')
    parser.add_argument('--web', action='store_true', help='Run with web interface')
    parser.add_argument('--dir', type=str, help='Directory to organize')
    parser.add_argument('--type', choices=['extension', 'timeline', 'semantic', 'intent'], 
                       default='extension', help='Organization type')
    
    args = parser.parse_args()
    
    # Web interface mode
    if args.web:
        try:
            from web.app import start_web_app
            print("Starting web interface...")
            start_web_app()
        except ImportError as e:
            print(f"Error: Web interface dependencies not found. {e}")
            print("Please install Flask with: pip install flask")
            sys.exit(1)
        return
    
    # GUI mode (default if no arguments provided)
    if args.gui or not (args.cli or args.web):
        try:
            import tkinter as tk
            from gui.neurotask_ui import NeurotaskUI
            root = tk.Tk()
            app = NeurotaskUI(root)
            root.mainloop()
        except ImportError:
            print("Error: Tkinter is required for GUI mode. Please install it or use CLI mode.")
            sys.exit(1)
        return
    
    # CLI mode (if --cli specified or --dir provided)
    if args.cli or args.dir:
        if not args.dir:
            print("Error: Directory path (--dir) is required in CLI mode")
            sys.exit(1)
        
        # Import organizer modules based on the selected type
        try:
            if args.type == 'extension':
                from organizer.extension_based import organize_by_extension
                from config import load_config
                config = load_config()
                organize_by_extension(args.dir, config["file_categories"])
            elif args.type == 'timeline':
                from organizer.timeline_based import organize_by_timeline
                organize_by_timeline(args.dir)
            elif args.type == 'semantic':
                from organizer.semantic_based import organize_by_semantics
                organize_by_semantics(args.dir)
            elif args.type == 'intent':
                from organizer.intent_based import organize_by_intents
                organize_by_intents(args.dir)
            
            print(f"✅ Files organized using {args.type} method")
        except Exception as e:
            print(f"Error during organization: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()