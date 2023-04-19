import openai
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as tkst
import tkinter.simpledialog as tkdialog
import clipboard

# OpenAI API key
openai.api_key = "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"

# Create the GUI window
window = tk.Tk()
window.title("Random Code Generator")
window.configure(bg='#ADD8E6')


# Define the function for generating a random code
def generate_code():
    topic = topic_entry.get()
    language_name = language.get()
    prompt = f"Generate a {language_name} code about {topic}"
    model = "text-davinci-003"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=2500
    )
    code = response.choices[0].text.strip()
    response_text.delete('1.0', tk.END)
    response_text.insert(tk.END, code)

def copy_to_clipboard():
    selected_text = response_text.get("sel.first", "sel.last")
    if selected_text:
        clipboard.copy(selected_text) 

# Add an entry box for the topic
topic_label = tk.Label(window, text="Topic:")
topic_label.pack()
topic_entry = tk.Entry(window)
topic_entry.pack(pady=10)

# Add a drop-down list for programming language selection
language_options = ["Python", "Java", "JavaScript", "c++", "c#", "PHP", "Ruby", "Swift", "Go", "Rust", "Kotlin", "Dart", "Scala", "R", "C", "Objective-C", "Perl", "Haskell", "Lua", "Julia", "Clojure", "Elixir", "F#", "Groovy", "Matlab", "Visual Basic", "Assembly", "Ada", "COBOL", "D", "Erlang", "Fortran", "Lisp", "Logo", "Pascal", "Prolog", "Racket", "Scheme", "SQL", "TypeScript", "VBScript", "VHDL", "Verilog", "Visual Basic .NET", "Visual Basic Script", "Visual DataFlex", "Visual FoxPro", "Visual J#", "Visual J++", "Visual Objects", "Visual Prolog", "Visual Prolog .NET", "Visual Studio Tools for Applications", "Visual Studio Tools for Office", "Visual Studio .NET", "VisualWorks", "WebDNA", "WebQL", "WebObjects", "WebSphere"]
language = tk.StringVar(value=language_options[0])
language_dropdown = ttk.Combobox(window, textvariable=language, values=language_options)
language_dropdown.pack(pady=10)

# Add a button to the GUI window
button = tk.Button(window, text="Generate Code", command=generate_code)
button.pack(pady=10)

# Add a text widget for the response
response_text = tk.Text(window, height=20, width=80)
response_text.pack(pady=10)

# Add a scrollbar to the response text widget
scrollbar = tk.Scrollbar(window, command=response_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
response_text.config(yscrollcommand=scrollbar.set)

copy_button = tk.Button(window, text="Copy Selected Text", command=copy_to_clipboard)
copy_button.pack(pady=10)
copy_button.configure(bg='#ADD8E6')
# Run the GUI window
window.mainloop()
