import tkinter as tk

#Creating a window
window = tk.Tk()
window.title("System Configuration")
window.geometry("800x400")

#Create buttons to access different system info configurations
def systeminfo():
    window.withdraw() # Hide current window
    window1 = tk.Tk()
    window1.title("System Information")
    window1.geometry("400x200")
    label1 = tk.Label(window1, text="System Information")
    label1.grid(column=0, row=0)
    label2 = tk.Label(window1, text="System Information")
    label2.grid(column=0, row=1)
    exitButton = tk.Button(window1, text=" Exit ", command=closeWindow)
    exitButton.grid(column=0, row=2)
    window1.mainloop()

def hardwareinfo():
    window.withdraw() # Hide current window
    window2 = tk.Tk()
    window2.title("Hardware Information")
    window2.geometry("400x200")
    label1 = tk.Label(window2, text="Hardware Information")
    label1.grid(column=0, row=0)
    label2 = tk.Label(window2, text="Hardware Information")
    label2.grid(column=0, row=1)
    exitButton = tk.Button(window2, text=" Exit ", command=closeWindow)
    exitButton.grid(column=0, row=2)
    window2.mainloop()

def drivers():
    window.withdraw() # Hide current window
    window3 = tk.Tk()
    window3.title("Driver Information")
    window3.geometry("400x200")
    label1 = tk.Label(window3, text="Driver Information")
    label1.grid(column=0, row=0)
    label2 = tk.Label(window3, text="Driver Information")
    label2.grid(column=0, row=1)
    exitButton = tk.Button(window3, text=" Exit ", command=closeWindow)
    exitButton.grid(column=0, row=2)
    window3.mainloop()

def closeWindow():
   window.destroy()

infoButton = tk.Button(window, text="System Information", command=systeminfo)
infoButton.grid(column=0, row=0)

hardButton = tk.Button(window, text="Hardware Information", command=hardwareinfo)
hardButton.grid(column=0, row=1)

driverButton = tk.Button(window, text="Driver Information", command=drivers)
driverButton.grid(column=0, row=2)

exitButton = tk.Button(window, text=" Exit ", command=closeWindow)
exitButton.grid(column=0, row=3)

window.mainloop()