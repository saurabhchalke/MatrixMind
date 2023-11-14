import os
import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
from dotenv import load_dotenv
import threading

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Setup OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def query_openai(prompt, chat_history):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Loading...\n")
    try:
        # Using the GPT 3.5 Turbo by default, and using custom instructions to have extremely concise responses
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant. Please provide really concise responses."},
                {"role": "user", "content": prompt}
            ]
        )
        # Remove "Loading..." and display the response
        chat_history.delete("end-2c linestart", "end-1c")
        result = response.choices[0].message.content
        chat_history.insert(tk.END, f"Matrix Mind: {result}\n\n")
    except Exception as e:
        chat_history.delete("end-2c linestart", "end-1c")
        chat_history.insert(tk.END, f"An error occurred: {e}\n\n")
    finally:
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END)

def send_query(event=None):
    user_input = user_input_text.get("1.0", tk.END).strip()
    if user_input:
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"You: {user_input}\n")
        user_input_text.delete("1.0", tk.END)
        threading.Thread(target=query_openai, args=(user_input, chat_history), daemon=True).start()
        return 'break'

# Set up the main application window
root = tk.Tk()
root.title("Matrix Mind")
root.geometry("800x600")  # 4:3 aspect ratio

# Set the font color for a neon green and background color
neon_green = '#39FF14'
bg_color = 'black'
font_family = "Press Start 2P"
font_size = 12

# Create a ScrolledText widget for chat history
chat_history = scrolledtext.ScrolledText(root, state=tk.DISABLED, bg=bg_color, fg=neon_green, font=(font_family, font_size))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Text widget for user input
user_input_text = tk.Text(root, height=5, bg=bg_color, fg=neon_green, font=(font_family, font_size))
user_input_text.pack(padx=10, pady=10, fill=tk.X, expand=False)
user_input_text.bind("<Return>", send_query)
user_input_text.bind("<KeyRelease-Return>", lambda e: "break")

# Blinking cursor effect
def cursor_blink():
    if user_input_text['insertbackground'] == neon_green:
        user_input_text.config(insertbackground=bg_color)
    else:
        user_input_text.config(insertbackground=neon_green)
    root.after(530, cursor_blink)

cursor_blink()

# Start the GUI event loop
root.mainloop()

