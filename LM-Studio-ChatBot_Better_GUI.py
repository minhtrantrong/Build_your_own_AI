import tkinter as tk
import customtkinter as ctk
import openai
from datetime import datetime
import time
import threading

openai.api_base = 'http://localhost:1234/v1'
openai.api_key = ''

prefix = "### Instruction:\n"
suffix = "\n### Response:"

def get_completion(prompt, model="local model", temperature=0.0):
    formatted_prompt = f"{prefix}{prompt}{suffix}"
    messages = [{"role": "user", "content": formatted_prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

class ModernChatbot:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Modern AI Chatbot")
        self.window.geometry("800x600")
        
        # Configure grid
        self.window.grid_rowconfigure(1, weight=1)  
        self.window.grid_columnconfigure(0, weight=1)
        
        # Create menu bar
        self.menu_bar = ctk.CTkFrame(self.window)
        self.menu_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Create theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.menu_bar,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(side="left", padx=10)
        
        # Create clear button
        self.clear_button = ctk.CTkButton(
            self.menu_bar,
            text="Clear History",
            command=self.clear_history,
            width=100
        )
        self.clear_button.pack(side="left", padx=10)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create chat display
        self.chat_display = ctk.CTkTextbox(
            self.main_frame,
            wrap="word",
            font=("Arial", 12),
        )
        self.chat_display.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.chat_display.configure(state="disabled")
        
        # Create input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Create message input
        self.message_input = ctk.CTkTextbox(
            self.input_frame,
            height=40,
            font=("Arial", 12),
        )
        self.message_input.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Create send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            command=self.send_message,
            width=100
        )
        self.send_button.grid(row=0, column=1)
        
        # Bind Return key
        self.message_input.bind("<Return>", self.handle_enter)
        
        # Initialize waiting animation state
        self.waiting_animation = False
        self.dots_count = 0
        self.waiting_text_position = None
        
        # Store chat history
        self.chat_history = []
        
        # Set initial theme and colors
        self.current_theme = "dark"
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        self.theme_switch.select()  
        self.update_text_colors()

    def toggle_theme(self):
        self.current_theme = "dark" if self.theme_switch.get() == "dark" else "light"
        ctk.set_appearance_mode(self.current_theme)
        self.update_text_colors()

    def update_text_colors(self):
        if self.current_theme == "dark":
            self.chat_display.tag_config("user", foreground="#ffffff")
            self.chat_display.tag_config("bot", foreground="#a0a0a0")
            self.chat_display.tag_config("time", foreground="#666666")
            self.chat_display.tag_config("waiting", foreground="#4a9eff")
        else:
            self.chat_display.tag_config("user", foreground="#000000")
            self.chat_display.tag_config("bot", foreground="#444444")
            self.chat_display.tag_config("time", foreground="#666666")
            self.chat_display.tag_config("waiting", foreground="#0066cc")

    def clear_history(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.chat_history = []

    def animate_waiting(self):
        while self.waiting_animation:
            if self.waiting_text_position:
                self.chat_display.configure(state="normal")
                self.chat_display.delete(self.waiting_text_position, f"{self.waiting_text_position} lineend")
                dots = "." * ((self.dots_count % 3) + 1)
                self.chat_display.insert(self.waiting_text_position, f"Waiting for response{dots}")
                self.chat_display.configure(state="disabled")
                self.dots_count += 1
                self.window.update()
            time.sleep(0.5)

    def add_message(self, message, is_user=True):
        self.chat_display.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add newline if there's already content
        if self.chat_display.get("1.0", "end-1c"):
            self.chat_display.insert("end", "\n")
        
        # Insert timestamp
        self.chat_display.insert("end", f"({timestamp}) ", "time")
        
        # Insert sender and message
        sender = "You: " if is_user else "Chatbot: "
        tag = "user" if is_user else "bot"
        self.chat_display.insert("end", sender, tag)
        self.chat_display.insert("end", message, tag)
        
        # Store in chat history
        self.chat_history.append({
            "time": timestamp,
            "sender": "user" if is_user else "bot",
            "message": message
        })
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def send_message(self):
        message = self.message_input.get("1.0", "end-1c").strip()
        if message:
            # Clear input immediately
            self.message_input.delete("1.0", "end")
            # Reset cursor position
            self.message_input.mark_set("insert", "1.0")
            # Update the GUI to show cleared input
            self.window.update()
            
            # Add user message
            self.add_message(message, is_user=True)
            
            # Start waiting animation
            self.chat_display.configure(state="normal")
            if self.chat_display.get("1.0", "end-1c"):
                self.chat_display.insert("end", "\n")
            self.chat_display.insert("end", f"({datetime.now().strftime('%H:%M')}) ", "time")
            self.chat_display.insert("end", "Chatbot: ", "bot")
            self.waiting_text_position = self.chat_display.index("end-1c")
            self.chat_display.insert("end", "Waiting for response...", "waiting")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")
            
            # Start animation in separate thread
            self.waiting_animation = True
            threading.Thread(target=self.animate_waiting, daemon=True).start()
            
            # Get response in separate thread
            def get_response():
                prompt = f"Assume that you are a virtual tutor assistant. Try to answer the question below in a simple way. Question: {message}"
                response = get_completion(prompt, temperature=0.2)
                
                # Stop animation
                self.waiting_animation = False
                
                # Update with response
                self.window.after(0, lambda: self.update_with_response(response))
            
            threading.Thread(target=get_response, daemon=True).start()

    def update_with_response(self, response):
        # Remove waiting message
        self.chat_display.configure(state="normal")
        self.chat_display.delete(f"{self.waiting_text_position} linestart", "end")
        self.chat_display.configure(state="disabled")
        
        # Add actual response
        self.add_message(response, is_user=False)
        
        # Focus back to input
        self.message_input.focus()

    def handle_enter(self, event):
        if not event.state & 0x1:  
            self.send_message()
            return "break"
        return None
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernChatbot()
    app.run()