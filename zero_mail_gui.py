import customtkinter as ctk
import threading
import time
import math
import socket
import urllib.request
import json
import sqlite3
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Mail - SMTP Client")
        self.geometry("800x600")
        self.configure(fg_color="#1a1a24")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Zero Mail - SMTP Client", font=("Helvetica", 24, "bold"), text_color="#00C7FF")
        self.header.pack(pady=20)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_ui()
        
    
    def setup_ui(self):
        self.inbox = ctk.CTkTextbox(self.main_frame, height=200)
        self.inbox.pack(fill=ctk.X, pady=10)
        self.inbox.insert("0.0", "Inbox:\n1. Welcome to Zero Mail!\n2. Your security alert\n")
        
        self.compose = ctk.CTkTextbox(self.main_frame)
        self.compose.pack(fill=ctk.BOTH, expand=True, pady=10)
        self.compose.insert("0.0", "To: user@example.com\nSubject: Hello\n\nMessage body here...")
        
        ctk.CTkButton(self.main_frame, text="Send Email", command=self.send).pack(pady=10)
        
    def send(self):
        self.header.configure(text="Email Sent (Simulated)!")
        self.compose.delete("0.0", "end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
