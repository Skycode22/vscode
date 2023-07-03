import openai
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as tkst
import tkinter.simpledialog as tkdialog
import clipboard
import math
def get_api_key():
    api_key = tkdialog.askstring("API Key", "Please enter your API key:")
    if api_key is None:
        messagebox.showerror("Error", "API key is required to proceed.")
        window.quit()
    return api_key
openai.api_key = get_api_key()
window = tk.Tk()
window.title("Random Code Generator")
window.configure(bg='#ADD8E6')
window.configure(borderwidth=15, relief=tk.RIDGE)
def generate_code():
    topic = topic_entry.get("1.0", tk.END).strip()
    language_name = language.get()
    prompt = f"Generate a {language_name} code about {topic}"
    model = "text-davinci-003"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=2500)
    code = response.choices[0].text.strip()
    response_text.delete('1.0', tk.END)
    response_text.insert(tk.END, code)
def copy_to_clipboard():
    selected_text = response_text.get("sel.first", "sel.last")
    if selected_text:
        clipboard.copy(selected_text)         
def validate_topic_input(input):
    lines = [input[i:i+30] for i in range(0, len(input), 30)]
    topic_entry.delete(0, tk.END)
    topic_entry.insert(0, '\n'.join(lines))
    return True       
def on_entry_keyrelease(event):
    text = topic_entry.get()
    lines = text.split('\n')
    num_lines = len(lines)
    longest_line = max(lines, key=len)
    width = max(10000, len(longest_line))
    topic_entry.config(width=width, height=num_lines)
topic_label = tk.Label(window, text="Topic:")
topic_label.grid(row=0, column=0, padx=10, pady=10, sticky='n')
topic_entry = tk.Text(window, width=80, height=1)
topic_entry.grid(row=3, column=0, padx=10, pady=10, sticky='ns')
topic_label.configure(bg='#FFFF00')
topic_label.configure(relief=tk.GROOVE)
language_options = ["Python", "Java", "JavaScript", "c++", "c#", "PHP", "Ruby", "Swift", "Go", "Rust", "Kotlin", "Dart", "Scala", "R", "C", "Objective-C", "Perl", "Haskell", "Lua", "Julia", "Clojure", 
                    "Elixir", "F#", "Groovy", "Matlab", "Visual Basic", "Assembly", "Ada", "COBOL", "D", "Erlang", "Fortran", "Lisp", "Logo", "Pascal", "Prolog", "Racket", "Scheme", "SQL", "TypeScript", 
                    "VBScript", "VHDL", "Verilog", "Visual Basic .NET", "Visual Basic Script", "Visual DataFlex", "Visual FoxPro", "Visual J#", "Visual J++", "Visual Objects", "Visual Prolog", "Visual Prolog .NET", 
                    "Visual Studio Tools for Applications", "Visual Studio Tools for Office", "Visual Studio .NET", "VisualWorks", "WebDNA", "WebQL", "WebObjects", "WebSphere"]
language = tk.StringVar(value=language_options[0])
language_label = tk.Label(window, text="Language Selection:")
language_label.configure(bg='#8FBC8F', relief=tk.RAISED)
language_label.grid(row=1, column=0, padx=10, pady=10, sticky='s')
language_dropdown = ttk.Combobox(window, textvariable=language, values=language_options)
language_dropdown.grid(row=2, column=0, padx=10, pady=10, sticky='s')
button = tk.Button(window, text="Generate Code", command=generate_code)
button.grid(row=2, column=1, pady=10, sticky='news')
button.configure(bg = '#8FBC8F')
button.configure(borderwidth=5, relief=tk.RIDGE)
response_text = tk.Text(window)
response_text.grid(row=3, column=1, padx=10, pady=10, sticky='news')
scrollbar = tk.Scrollbar(window, command=response_text.yview)
scrollbar.grid(row=3, column=2, sticky='ns')
response_text.config(yscrollcommand=scrollbar.set)
copy_button = tk.Button(window, text="Copy Selected Text", command=copy_to_clipboard)
copy_button.grid(row=4, column=1, pady=10)
copy_button.configure(bg='#8FBC8F')
copy_button.configure(borderwidth=5, relief=tk.RIDGE)
window.mainloop()
