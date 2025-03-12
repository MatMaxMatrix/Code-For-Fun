#!/usr/bin/env python3
# fixed_app.py - Fixed version of image_analysis_chatbot.py
import sys
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import os
from PIL import Image, ImageTk

# Define a simplified version of the chatbot
class SimpleImageAnalysisChatBot:
    def __init__(self, tk_root):
        self.root = tk_root
        self.root.title("Simple Image Analysis ChatBot")
        self.root.geometry("800x600")
        
        # Variables for the image
        self.image_path = ""
        self.thumbnail = None
        
        # Create the UI
        self.create_widgets()
    
    def create_widgets(self):
        # Top frame for image selection
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Button to select image
        self.select_btn = tk.Button(top_frame, text="Select Image", command=self.select_image)
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        # Label to show selected image path
        self.path_label = tk.Label(top_frame, text="No image selected")
        self.path_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Frame for image thumbnail
        self.img_frame = tk.Frame(self.root, width=200, height=200, bg="lightgray")
        self.img_frame.pack(side=tk.TOP, padx=10, pady=5)
        
        # Label for thumbnail
        self.img_label = tk.Label(self.img_frame, text="Image will appear here")
        self.img_label.pack(expand=True)
        
        # Chat area
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text widget for chat
        self.chat_text = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for chat
        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.config(yscrollcommand=scrollbar.set)
        
        # Input area
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Entry for user input
        self.user_input = tk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind("<Return>", self.on_enter_pressed)
        
        # Send button
        send_btn = tk.Button(input_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add initial message
        self.add_message("System", "Welcome to the Image Analysis ChatBot! Select an image and start chatting.")
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            self.image_path = file_path
            self.path_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.load_thumbnail()
            self.add_message("System", f"Image loaded: {os.path.basename(file_path)}")
    
    def load_thumbnail(self):
        try:
            # Open the image and create a thumbnail
            img = Image.open(self.image_path)
            img.thumbnail((200, 200))
            self.thumbnail = ImageTk.PhotoImage(img)
            
            # Update the image label
            self.img_label.config(image=self.thumbnail, text="")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def add_message(self, sender, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
    
    def send_message(self):
        message = self.user_input.get().strip()
        if message:
            self.add_message("You", message)
            self.user_input.delete(0, tk.END)
            
            # Simple response
            if self.image_path:
                response = f"I see you've loaded an image ({os.path.basename(self.image_path)}). Your message was: {message}"
            else:
                response = f"You haven't loaded an image yet. Your message was: {message}"
            
            self.add_message("Bot", response)
    
    def on_enter_pressed(self, event):
        self.send_message()
        return "break"

# Main application
try:
    print("Starting fixed_app.py")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Tkinter version: {tk.TkVersion}")
    
    # Create the main window
    root = tk.Tk()
    
    # Create the application
    app = SimpleImageAnalysisChatBot(root)
    
    print("Starting mainloop...")
    root.mainloop()
    print("Mainloop ended")

except Exception as e:
    print(f"ERROR: {e}")
    print("Traceback:")
    traceback.print_exc() 