#!/usr/bin/env python3
# debug_app.py - Debug version of image_analysis_chatbot.py
import sys
import traceback

# Add debug prints
print("Starting debug_app.py")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    print("Importing tkinter...")
    import tkinter as tk
    print(f"Tkinter version: {tk.TkVersion}")
    
    print("Importing other modules...")
    from tkinter import filedialog, messagebox
    import base64
    
    print("Checking for tkinterdnd2...")
    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
        USE_DND = True
        print("tkinterdnd2 imported successfully")
    except ImportError as e:
        USE_DND = False
        print(f"tkinterdnd2 import error: {e}")
    
    print("Importing PIL...")
    from PIL import Image, ImageTk
    print(f"PIL version: {Image.__version__}")
    
    import os
    
    # Import the main application
    print("Importing ImageAnalysisChatBot...")
    from image_analysis_chatbot import ImageAnalysisChatBot
    
    # Main application with debug
    print("Starting main application...")
    if USE_DND:
        print("Using TkinterDnD.Tk()")
        root = TkinterDnD.Tk()
    else:
        print("Using tk.Tk()")
        root = tk.Tk()
    
    # Check if we should use the real model or dummy model
    use_real_model = os.environ.get("USE_REAL_MODEL", "0") == "1"
    print(f"use_real_model: {use_real_model}")
    
    if use_real_model:
        try:
            print("Importing real_model_integration...")
            from real_model_integration import real_model
            print("Creating app with real model...")
            app = ImageAnalysisChatBot(root, chat_gpt_fn=real_model)
            print("Using real OpenAI model for chat")
        except ImportError as e:
            print(f"Error importing real model: {e}")
            print("Creating app with dummy model...")
            app = ImageAnalysisChatBot(root)
            print("Using dummy model for chat")
    else:
        print("Creating app with dummy model...")
        app = ImageAnalysisChatBot(root)
        print("Using dummy model for chat")
    
    print("Starting mainloop()...")
    root.mainloop()
    print("Mainloop ended")

except Exception as e:
    print(f"ERROR: {e}")
    print("Traceback:")
    traceback.print_exc() 