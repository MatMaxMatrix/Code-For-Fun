#!/usr/bin/env python3
# test_tkinter.py - Simple tkinter test
import sys
import tkinter as tk
from tkinter import messagebox

def show_message():
    messagebox.showinfo("Test", "Button clicked!")

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Tkinter version: {tk.TkVersion}")

# Create the main window
root = tk.Tk()
root.title("Tkinter Test")
root.geometry("400x300")

# Add a label
label = tk.Label(root, text="This is a test of tkinter", font=("Arial", 14))
label.pack(pady=20)

# Add a button
button = tk.Button(root, text="Click Me", command=show_message)
button.pack(pady=10)

# Add a quit button
quit_button = tk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(pady=10)

print("Starting mainloop...")
root.mainloop()
print("Mainloop ended") 