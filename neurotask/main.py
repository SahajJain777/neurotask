# main.py
import os
import sys

# Add parent directory to path so 'neurotask' can be found
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
print(f"[DEBUG] Added to Python path: {parent_dir}")

import argparse
import tkinter as tk
from neurotask.utils.logger import setup_logger

# Setup logging
logger = setup_logger("neurotask")

def main():
    """Main entry point for the application"""
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

        logger.info("🧠 Neurotask running with Python: %s", sys.version.split()[0])
        logger.info("📍 Interpreter: %s", sys.executable)

        parser = argparse.ArgumentParser(description='Neurotask File Organizer')
        parser.add_argument('--cli', action='store_true', help='Run in command line mode')
        parser.add_argument('--gui', action='store_true', help='Run with graphical user interface')
        parser.add_argument('--dir', type=str, help='Directory to organize')
        parser.add_argument('--type', choices=['extension', 'timeline', 'semantic', 'intent'], 
                           default='extension', help='Organization type')
        parser.add_argument('--voice', action='store_true', 
                           help='Enable voice assistant in GUI mode')
        parser.add_argument('--no-voice', action='store_true', 
                           help='Disable voice assistant in GUI mode')

        args = parser.parse_args()

        # GUI mode
        if args.gui or not args.cli:
            try:
                from neurotask.gui.neurotask_ui import NeurotaskUI
                root = tk.Tk()
                
                try:
                    root.iconbitmap('assets/icon.ico')
                except Exception as e:
                    logger.warning("Could not load icon: %s", str(e))
                    
                voice_enabled = not args.no_voice
                if args.voice:
                    voice_enabled = True
                    
                app = NeurotaskUI(root, voice_enabled=voice_enabled)
                root.mainloop()
            except ImportError as e:
                logger.error("Failed to import GUI components: %s", str(e))
                sys.exit(1)
            except Exception as e:
                logger.error("Failed to launch GUI: %s", str(e))
                sys.exit(1)
            return

        # CLI mode
        if args.cli or args.dir:
            try:
                # Import CLI components
                from neurotask.organizer import extension_based, timeline_based, semantic_based, intent_based
                from neurotask.utils.config import load_config
                
                if not args.dir:
                    logger.error("Directory argument required for CLI mode")
                    sys.exit(1)
                    
                if not os.path.isdir(args.dir):
                    logger.error("Invalid directory: %s", args.dir)
                    sys.exit(1)
                
                # Perform organization based on type
                if args.type == "extension":
                    config = load_config()
                    extension_based.organize_by_extension(args.dir, config["file_categories"])
                elif args.type == "timeline":
                    timeline_based.organize_by_timeline(args.dir)
                elif args.type == "semantic":
                    semantic_based.organize_by_semantics(args.dir)
                elif args.type == "intent":
                    intent_based.organize_by_intents(args.dir)
                    
                logger.info("Organization completed successfully")
            except Exception as e:
                logger.error("CLI operation failed: %s", str(e))
                sys.exit(1)
    except Exception as e:
        logger.error("Fatal error: %s", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()