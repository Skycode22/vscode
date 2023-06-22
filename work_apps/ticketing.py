import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import pickle

class Ticket:
    def __init__(self, name, problem):
        self.name = name
        self.problem = problem
        self.date = datetime.now()

class TicketingSystem:
    def __init__(self):
        self.load_tickets()

    def add_ticket(self, ticket):
        self.active_tickets.append(ticket)
        self.save_tickets()

    def archive_ticket(self, ticket):
        self.active_tickets.remove(ticket)
        self.archived_tickets.append(ticket)
        self.save_tickets()

    def delete_ticket(self, ticket, archived=False):
        if archived:
            self.archived_tickets.remove(ticket)
        else:
            self.active_tickets.remove(ticket)
        self.save_tickets()

    def load_tickets(self):
        try:
            with open('tickets.pkl', 'rb') as f:
                self.active_tickets, self.archived_tickets = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.active_tickets = []
            self.archived_tickets = []

    def save_tickets(self):
        with open('tickets.pkl', 'wb') as f:
            pickle.dump((self.active_tickets, self.archived_tickets), f)

class App:
    def __init__(self, root, ticketing_system):
        self.root = root
        self.ticketing_system = ticketing_system

        self.root.title('Ticketing System')
        self.root.configure(bg='dark grey')  # Set the background color to dark grey

        self.name_text = tk.StringVar()
        self.problem_text = tk.StringVar()

        self.name_frame = tk.Frame(root, borderwidth=2, relief='groove', bg='dark grey')  # Set the background color to dark grey
        self.name_frame.pack(pady=5)
        self.name_label = tk.Label(self.name_frame, text="Enter your name:", font=('Arial', 14), bg='lightblue')
        self.name_label.pack(side='left')
        self.name_entry = tk.Entry(self.name_frame, textvariable=self.name_text, font=('Arial', 14))
        self.name_entry.pack(side='left')

        self.problem_frame = tk.Frame(root, borderwidth=2, relief='groove', bg='dark grey')  # Set the background color to dark grey
        self.problem_frame.pack(pady=5)
        self.problem_label = tk.Label(self.problem_frame, text="Enter your problem:", font=('Arial', 14), bg='lightblue')
        self.problem_label.pack(side='left')
        self.problem_entry = tk.Entry(self.problem_frame, textvariable=self.problem_text, font=('Arial', 14))
        self.problem_entry.pack(side='left')

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_ticket, font=('Arial', 14))
        self.submit_button.pack(pady=5)

        self.root.bind('<Return>', self.submit_ticket)  # Bind the 'Enter' key to the submit_ticket function

        self.ticket_canvas = tk.Canvas(root, bg='dark grey')  # Set the background color to dark grey
        self.ticket_frame = tk.Frame(self.ticket_canvas, bg='dark grey')  # Set the background color to dark grey
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.ticket_canvas.yview)
        self.ticket_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.ticket_canvas.pack(side=        "top", fill="both", expand=True)
        self.ticket_canvas.create_window((0,0), window=self.ticket_frame, anchor='n')

        self.ticket_frame.bind("<Configure>", lambda e: self.ticket_canvas.configure(scrollregion=self.ticket_canvas.bbox("all")))

        self.archive_button = tk.Button(root, text="View Archived Tickets", command=self.view_archived_tickets, font=('Arial', 14))
        self.archive_button.pack(pady=5)

        self.update_ticket_view()

    def submit_ticket(self, event=None):  # Add an optional event parameter to handle the 'Enter' key press
        name = self.name_text.get()
        problem = self.problem_text.get()
        if name and problem:
            ticket = Ticket(name, problem)
            self.ticketing_system.add_ticket(ticket)
            messagebox.showinfo("Success", "Ticket submitted successfully!")
            self.name_text.set("")
            self.problem_text.set("")
            self.update_ticket_view()
        else:
            messagebox.showerror("Error", "Name and problem description cannot be empty.")

    def update_ticket_view(self):
        for widget in self.ticket_frame.winfo_children():
            widget.destroy()

        for i, ticket in enumerate(self.ticketing_system.active_tickets, 1):
            label = tk.Label(self.ticket_frame, text=f"#{i}. For: {ticket.name} on {ticket.date.strftime('%Y-%m-%d %H:%M:%S')}: {ticket.problem}", font=('Arial', 12), bg='dark grey')  # Set the background color to dark grey
            label.grid(row=i, column=0, sticky='w')
            archive_button = tk.Button(self.ticket_frame, text="Archive", command=lambda t=ticket: self.archive_ticket(t), font=('Arial', 12))
            archive_button.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            delete_button = tk.Button(self.ticket_frame, text="Delete", command=lambda t=ticket: self.delete_ticket(t), font=('Arial', 12))
            delete_button.grid(row=i, column=2, padx=5, pady=2, sticky='w') 
        self.ticket_canvas.configure(scrollregion=self.ticket_canvas.bbox('all'))

    def archive_ticket(self, ticket):
        self.ticketing_system.archive_ticket(ticket)
        self.update_ticket_view()

    def delete_ticket(self, ticket):
        self.ticketing_system.delete_ticket(ticket)
        self.update_ticket_view()

    def view_archived_tickets(self):
        window = tk.Toplevel(self.root)
        window.title('Archived Tickets')
        window.configure(bg='dark grey')  # Set the background color to dark grey
        for i, ticket in enumerate(self.ticketing_system.archived_tickets, 1):
            label = tk.Label(window, text=f"Archived Ticket {i} by {ticket.name} on {ticket.date.strftime('%Y-%m-%d %H:%M:%S')}: {ticket.problem}", font=('Arial', 12), bg='dark grey')  # Set the background color to dark grey
            label.pack(pady=5)
            delete_button = tk.Button(window, text="Delete", command=lambda t=ticket: self.delete_archived_ticket(t, window), font=('Arial', 12))
            delete_button.pack(pady=5)

    def delete_archived_ticket(self, ticket, window):
        self.ticketing_system.delete_ticket(ticket, archived=True)
        window.destroy()
        self.view_archived_tickets()

def main():
    root = tk.Tk()
    root.geometry('750x750')
    ticketing_system = TicketingSystem()
    app = App(root, ticketing_system)
    root.mainloop()

if __name__ == "__main__":
    main()
