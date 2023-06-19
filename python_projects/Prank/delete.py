import tkinter as tk
from tkinter import ttk
import subprocess
import sys

def start_progress(value=0):
    progress['value'] = value
    percent_label['text'] = "{}%".format(value)
    if value < 100:
        root.after(1000, start_progress, value+1)

def restart_program():
    python = sys.executable
    subprocess.call([python, __file__])

root = tk.Tk()
root.title("Destoy")
root.geometry("522x650")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

image = tk.PhotoImage(file="img2.png")

image_label = tk.Label(frame, image=image)
image_label.grid(column=1, row=0, sticky=(tk.W, tk.E))

progress = ttk.Progressbar(frame, length=200, mode='determinate')
progress.grid(column=1, row=1, sticky=(tk.W, tk.E))

percent_label = tk.Label(frame, text="0%")
percent_label.grid(column=1, row=2, sticky=(tk.W, tk.E))

text_label = tk.Label(frame, text="Deleting files and directories on server(s) 192.168.254.*")
text_label.grid(column=1, row=3, sticky=(tk.W, tk.E))

root.protocol("WM_DELETE_WINDOW", restart_program)
root.after(0, start_progress)

root.mainloop()
