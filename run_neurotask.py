#!/usr/bin/env python
# run_neurotask.py - Launcher script for Neurotask application

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
print(f"[DEBUG] Setting Python path: {project_root}")

# Import and run the main function
try:
    from neurotask.main import main
    main()
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("\nTry running the debug_imports.py script to diagnose path issues:")
    print("python debug_imports.py")
    sys.exit(1)
except Exception as e:
    import traceback
    print(f"Error running application: {e}")
    traceback.print_exc()
    sys.exit(1) 