import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from openai import OpenAI

# Put your URI end point:port here for your local inference server (in LM Studio) 
client = OpenAI(
    base_url='http://localhost:1234/v1',
    # Define the API key, required but ignored
    api_key='',
)

# Adjust the following based on the model type
# Alpaca style prompt format:
prefix = "### Instruction:\n" 
suffix = "\n### Response:"

# 'Llama2 Chat' prompt format:
# prefix = "[INST]"
# suffix = "[/INST]"

# Define the chatbot model and promt format
def get_completion(prompt, model="local model", temperature=0.0):
    formatted_prompt = f"{prefix}{prompt}{suffix}"
    messages = [{"role": "user", "content": formatted_prompt}]
    # print(f'\nYour prompt: {prompt}\n')
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


def send_message():
    INSTRUCTION = "Assume that you are a virtual tutor assistant. Try to answer the question below in a simple way. "
    user_input = user_entry.get("1.0", tk.END).strip()
    if user_input:
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"You: {user_input}\n")
        chat_history.config(state=tk.DISABLED)
        # Combine prompt and get chat completion
        prompt = f"{INSTRUCTION}. Question: {user_input}"
        response = get_completion(prompt, temperature=0.2)
        # Update the chat history
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"Chatbot: {response}\n")
        chat_history.config(state=tk.DISABLED)
        user_entry.delete("1.0", tk.END)
        chat_history.see(tk.END)

# Create the main window
window = tk.Tk()
window.title("Chatbot")

# Create the chat history box
chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=40)
chat_history.pack()
chat_history.config(state=tk.DISABLED)

# Create the user input entry
user_entry = tk.Text(window, height=1, width=50)
user_entry.pack()

# Create the send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Run the GUI
window.mainloop()