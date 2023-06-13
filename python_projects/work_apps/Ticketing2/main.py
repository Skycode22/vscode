import tkinter as tk
from tkinter import messagebox, simpledialog

class Ticket:
    id_counter = 1

    def __init__(self, employee_name, issue):
        self.id = Ticket.id_counter
        Ticket.id_counter += 1
        self.employee_name = employee_name
        self.issue = issue
        self.status = "open"

    def __str__(self):
        return f"Ticket id: {self.id}, Employee Name: {self.employee_name}, Issue: {self.issue}, Status: {self.status}"

class TicketingSystem:
    def __init__(self):
        self.tickets = {}

    def create_ticket(self, employee_name, issue):
        ticket = Ticket(employee_name, issue)
        self.tickets[ticket.id] = ticket
        return ticket.id

    def list_tickets(self):
        return '\n'.join(str(ticket) for ticket in self.tickets.values())

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.ticketing_system = TicketingSystem()
        self.create_widgets()

    def create_widgets(self):
        self.create_ticket_button = tk.Button(self)
        self.create_ticket_button["text"] = "Create Ticket"
        self.create_ticket_button["command"] = self.create_ticket
        self.create_ticket_button.pack(side="top")

        self.view_tickets_button = tk.Button(self)
        self.view_tickets_button["text"] = "View Tickets"
        self.view_tickets_button["command"] = self.view_tickets
        self.view_tickets_button.pack(side="top")

        self.quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit_button.pack(side="bottom")

    def create_ticket(self):
        employee_name = simpledialog.askstring("Input", "Enter employee name:", parent=self.master)
        issue = simpledialog.askstring("Input", "Enter issue:", parent=self.master)
        self.ticketing_system.create_ticket(employee_name, issue)

    def view_tickets(self):
        messagebox.showinfo("Tickets", self.ticketing_system.list_tickets())

root = tk.Tk()
app = Application(master=root)
app.mainloop()
