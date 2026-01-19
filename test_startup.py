import tkinter as tk
import sys
import os

# Ensure current directory is in path
sys.path.append(os.getcwd())

try:
    from main import CalculadoraApp
    print("Import successful")
    root = tk.Tk()
    app = CalculadoraApp(root)
    # Force update to ensure widgets are created and styles applied
    root.update() 
    print("Startup successful")
    root.destroy()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
