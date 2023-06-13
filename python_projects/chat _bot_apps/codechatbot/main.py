import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import messagebox
import openai
import os
import subprocess
import sys
from io import StringIO
from contextlib import redirect_stdout
import executing


# Replace with your actual API key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


class Chatbot:
    def __init__(self):
        self.conversation_history = []

    def handle_code_snippet(self, code):
        try:
            result = subprocess.run(
                ["python", "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=True,
                encoding="utf-8"
            )
            output = result.stdout
        except subprocess.TimeoutExpired:
            output = "Code execution timed out"
        except subprocess.CalledProcessError as e:
            output = f"Code execution failed: {e.stderr}"
        except Exception as e:
            output = f"Error: {e}"
        
        return output

    def generate_gpt3_response(self, message):
        prompt = f"{message}\nChatbot:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].text.strip()

    def chat(self, message):
        print(f"Message: {message}")

        if message.startswith("```") and message.endswith("```"):
            code = message[3:-3]
            result = self.handle_code_snippet(code)
            response = f"Code executed. Output:\n{result}"
        else:
            response = self.generate_gpt3_response(message)

        self.conversation_history.append((message, response))
        return response

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.chatbot = Chatbot()
        self.conversations = []
        self.current_conversation = []

        # Create sidebar
        self.sidebar = ttk.Frame(root, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Create main content area
        self.content = ttk.Frame(root)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.new_conversation()

    def create_widgets(self):
        # Create "New Conversation" button
        self.new_conversation_button = ttk.Button(
            self.sidebar, text="New Conversation", command=self.new_conversation
        )
        self.new_conversation_button.pack(padx=10, pady=10)

        # Create conversation history list
        self.conversations_listbox = tk.Listbox(self.sidebar)
        self.conversations_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.conversations_listbox.bind(
            "<<ListboxSelect>>", self.select_conversation
        )

        # Create conversation display
        self.conversation_display = scrolledtext.ScrolledText(
            self.content, wrap=tk.WORD, state="disabled"
        )
        self.conversation_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create message input
        self.message_input = ttk.Entry(self.content)
        self.message_input.pack(padx=10, pady=10, fill=tk.X, expand=False)
        self.message_input.focus()

                # Bind Enter key to send_message method
        self.root.bind("<Return>", self.send_message)

    def new_conversation(self):
        self.current_conversation = []
        self.conversations.append(self.current_conversation)
        conversation_id = len(self.conversations)
        self.conversations_listbox.insert(tk.END, f"Conversation {conversation_id}")

    def select_conversation(self, event=None):
        selection = event.widget.curselection()
        if selection:
            conversation_index = selection[0]
            self.current_conversation = self.conversations[conversation_index]
            self.update_conversation_display()

    def update_conversation_display(self):
        self.conversation_display.config(state="normal")
        self.conversation_display.delete("1.0", tk.END)
        for message, response in self.current_conversation:
            self.conversation_display.insert(tk.END, f"You: {message}\n")
            self.conversation_display.insert(tk.END, f"Chatbot: {response}\n")
        self.conversation_display.config(state="disabled")

    def handle_code_snippet(self, code):
        try:
            result = subprocess.run(
                ["python", "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=True,
                encoding="utf-8"
            )
            output = result.stdout
        except subprocess.TimeoutExpired:
            output = "Code execution timed out"
        except subprocess.CalledProcessError as e:
            output = f"Code execution failed: {e.stderr}"
        except Exception as e:
            output = f"Error: {e}"
        
        return output

    def generate_gpt3_response(self, message):
        prompt = f"{message}\nChatbot:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].text.strip()

    def chat(self, message):
        print(f"Message: {message}")

        if message.startswith("```") and message.endswith("```"):
            code = message[3:-3]
            result = self.handle_code_snippet(code)
            response = f"Code executed. Output:\n{result}"
        else:
            response = self.generate_gpt3_response(message)

        self.current_conversation.append((message, response))
        self.update_conversation_display()
        return response

    def handle_message(self, message):
        response = self.chat(message)
        self.conversation_display.config(state="normal")
        self.conversation_display.insert(tk.END, f"You: {message}\n")
        self.conversation_display.insert(tk.END, f"Chatbot: {response}\n")
        self.conversation_display.config(state="disabled")

    def send_message(self, event=None):
        if not self.current_conversation:
            self.new_conversation()

        message = self.message_input.get()

        if not message:
            return

        self.handle_message(message)

        self.message_input.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chatbot")
    root.geometry("800x600")

    chatbot_gui = ChatbotGUI(root)

    root.mainloop()
