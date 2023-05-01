import psutil
import tkinter as tk
from tkinter import ttk
import GPUtil

def update_utilization():
    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    gpu_percentages = [gpu.load * 100 for gpu in GPUtil.getGPUs()]

    cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
    ram_label.config(text=f"RAM Usage: {ram_percent}%")
    disk_label.config(text=f"Disk Usage: {disk_percent}%")

    for i, gpu_percent in enumerate(gpu_percentages):
        gpu_labels[i].config(text=f"GPU {i} Usage: {gpu_percent}%")

    root.after(1000, update_utilization)

root = tk.Tk()
root.title("Hardware Utilization")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

cpu_label = ttk.Label(frame)
cpu_label.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

ram_label = ttk.Label(frame)
ram_label.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

disk_label = ttk.Label(frame)
disk_label.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

gpus = GPUtil.getGPUs()
gpu_labels = []

for i, gpu in enumerate(gpus):
    gpu_label = ttk.Label(frame)
    gpu_label.grid(row=3+i, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
    gpu_labels.append(gpu_label)

root.after(1000, update_utilization)
root.mainloop()
