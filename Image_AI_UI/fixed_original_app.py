#!/usr/bin/env python3
# fixed_original_app.py - Fixed version of the original application without tkinterdnd2
import sys
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
from PIL import Image, ImageTk
import os

# Import the original ImageAnalysisChatBot class
from image_analysis_chatbot import ImageAnalysisChatBot

# Main application with error handling
try:
    print("Starting fixed_original_app.py")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Tkinter version: {tk.TkVersion}")
    
    # Create the main window without using tkinterdnd2
    print("Creating tk.Tk() without tkinterdnd2")
    root = tk.Tk()
    
    # Create the application
    print("Creating ImageAnalysisChatBot instance")
    app = ImageAnalysisChatBot(root)
    print("Using dummy model for chat")
    
    print("Starting mainloop...")
    root.mainloop()
    print("Mainloop ended")

except Exception as e:
    print(f"ERROR: {e}")
    print("Traceback:")
    traceback.print_exc() 