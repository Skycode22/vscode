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

        self.bg_image = tk.PhotoImage(file='bg.png')
        self.background_label = tk.Label(self.root, image=self.bg_image) 
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 
        
        self.name_text = tk.StringVar()
        self.problem_text = tk.StringVar()

        self.name_frame = tk.Frame(root, borderwidth=5, relief='groove', bg='lightblue')
        self.name_frame.pack(pady=5)
        self.name_label = tk.Label(self.name_frame, text="Employee:", font=('Gadugi', 14), bg='lightblue')
        self.name_label.pack(side='left')
        self.name_entry = tk.Entry(self.name_frame, textvariable=self.name_text, font=('Gadugi', 14), width=30)
        self.name_entry.pack(side='left')

        self.problem_frame = tk.Frame(root, borderwidth=5, relief='groove', bg='lightblue') 
        self.problem_frame.pack(pady=5)
        self.problem_label = tk.Label(self.problem_frame, text="Issue:", font=('Gadugi', 14), bg='lightblue')
        self.problem_label.pack(side='left')
        self.problem_entry = tk.Text(self.problem_frame, font=('Gadugi', 14), width=75, height=3)
        self.problem_entry.pack(side='left')
        
        self.submit_button = tk.Button(root, borderwidth=3, relief='ridge', text="Submit", command=self.submit_ticket, font=('Gadugi', 14), bg='#20B2AA')
        self.submit_button.pack(pady=5)
        self.root.bind('<Return>', self.submit_ticket)
        
        self.ticket_canvas = tk.Canvas(root, bg='light grey')  
        self.ticket_frame = tk.Frame(self.ticket_canvas, bg='light grey') 
        
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.ticket_canvas.yview)
        self.ticket_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.ticket_canvas.pack(side="top", fill="both", expand=True)
        self.ticket_canvas.create_window((0,0), window=self.ticket_frame, anchor='n')
        self.ticket_frame.bind("<Configure>", lambda e: self.ticket_canvas.configure(scrollregion=self.ticket_canvas.bbox("all")))

        self.archive_button = tk.Button(root,borderwidth=3, relief='ridge', text="View Archived Tickets", command=self.view_archived_tickets, font=('Gadugi', 14), bg='#FFFACD')
        self.archive_button.pack(pady=5)

        self.update_ticket_view()

    def submit_ticket(self, event=None):
        name = self.name_text.get()
        problem = self.problem_entry.get("1.0", tk.END).strip()
        if name and problem:
            ticket = Ticket(name, problem)
            self.ticketing_system.add_ticket(ticket)
            self.name_text.set("")
            self.problem_entry.delete("1.0", tk.END)
            self.update_ticket_view()
        else:
            messagebox.showerror("Error", "Name and problem description cannot be empty.")

    def update_ticket_view(self):
        for widget in self.ticket_frame.winfo_children():
            widget.destroy()

        for i, ticket in enumerate(self.ticketing_system.active_tickets, 1):
            label = tk.Label(
                self.ticket_frame,
                text=f"#{i}. For {ticket.name} on ({ticket.date.strftime('%Y-%m-%d, %H:%M')}) :{ticket.problem}",
                font=('Gadugi', 12, "bold"),
                bg='dark grey',
                wraplength=1000,
                anchor='center'  # Set the anchor to 'w' for left alignment
            )
            label.grid(row=i, column=3, sticky='w', padx=10, pady=5)  # Add padx for horizontal centering

            detail_button = tk.Button(self.ticket_frame, text="Details", font=('Gadugi', 12), bg='lightblue')
            detail_button.grid(row=i, column=4, padx=5, pady=2)

            detail_text = tk.Text(self.ticket_frame, font=('Gadugi', 12), width=40, height=3)
            detail_text.grid(row=i, column=3, sticky='w', columnspan=2)
            detail_text.grid_remove()  # Hide it initially

            detail_button['command'] = lambda t=detail_text: self.toggle_detail_text(t)

            archive_button = tk.Button(self.ticket_frame, text="Archive", command=lambda t=ticket: self.archive_ticket(t),
                                    font=('Gadugi', 12), bg='lightblue')
            archive_button.grid(row=i, column=2, padx=5, pady=2)
            delete_button = tk.Button(self.ticket_frame, text="Delete", command=lambda t=ticket: self.delete_ticket(t),
                                    font=('Gadugi', 12), bg='lightblue')
            delete_button.grid(row=i, column=1, padx=5, pady=2)

        self.ticket_canvas.configure(scrollregion=self.ticket_canvas.bbox('all'))

    def toggle_detail_text(self, detail_text):  
        if detail_text.winfo_viewable():
            detail_text.grid_remove()
        else:
            detail_text.grid()

    def archive_ticket(self, ticket):
        self.ticketing_system.archive_ticket(ticket)
        self.update_ticket_view()

    def delete_ticket(self, ticket):
        self.ticketing_system.delete_ticket(ticket)
        self.update_ticket_view()

    def view_archived_tickets(self):
        window = tk.Toplevel(self.root)
        window.title('Archived Tickets')
        window.configure(bg='light grey')
        for i, ticket in enumerate(self.ticketing_system.archived_tickets, 1):
            label = tk.Label(
                window,
                text=f"Archived Ticket {i} by {ticket.name} on {ticket.date.strftime('%Y-%m-%d %H:%M')}: {ticket.problem}",
                font=('Gadugi', 12),
                bg='dark grey'
            )
            label.pack(pady=5)

            detail_button = tk.Button(
                window,
                text="View Details",
                command=lambda t=ticket: self.view_archived_ticket_details(t, window),
                font=('Gadugi', 12),
                bg='lightblue'
            )
            detail_button.pack(pady=5)

    def view_archived_ticket_details(self, ticket, window):
        detail_window = tk.Toplevel(window)
        detail_window.title(f"Ticket Details - Archived Ticket by {ticket.name}")
        detail_window.configure(bg='light grey')

        detail_label = tk.Label(
            detail_window,
            text=f"Ticket details:\n\nName: {ticket.name}\nDate: {ticket.date.strftime('%Y-%m-%d %H:%M:%S')}\nProblem: {ticket.problem}",
            font=('Gadugi', 12),
            bg='light grey'
        )
        detail_label.pack(pady=10)

        delete_button = tk.Button(
            detail_window,
            text="Delete",
            command=lambda: self.delete_archived_ticket(ticket, window),
            font=('Gadugi', 12),
            bg='lightblue'
        )
        delete_button.pack(pady=5)

    def delete_archived_ticket(self, ticket, window):
        self.ticketing_system.delete_ticket(ticket, archived=True)
        window.destroy()
        self.view_archived_tickets()

    def view_archived_ticket_details(self, ticket, window):
        detail_window = tk.Toplevel(window)
        detail_window.title(f"Ticket Details - Archived Ticket by {ticket.name}")
        detail_window.configure(bg='light grey')

        detail_label = tk.Label(
            detail_window,
            text=f"Ticket details:\n\nName: {ticket.name}\nDate: {ticket.date.strftime('%Y-%m-%d %H:%M:%S')}\nProblem: {ticket.problem}",
            font=('Gadugi', 12),
            bg='light grey'
        )
        detail_label.pack(pady=10)

        unarchive_button = tk.Button(
            detail_window,
            text="Unarchive",
            command=lambda: self.unarchive_ticket(ticket),
            font=('Gadugi', 12),
            bg='lightblue'
        )
        unarchive_button.pack(pady=5)

        delete_button = tk.Button(
            detail_window,
            text="Delete",
            command=lambda: self.delete_archived_ticket(ticket, window),
            font=('Gadugi', 12),
            bg='lightblue'
        )
        delete_button.pack(pady=5)
        
    def unarchive_ticket(self, ticket):
        self.ticketing_system.archived_tickets.remove(ticket)
        self.ticketing_system.active_tickets.append(ticket)
        self.update_ticket_view()
      
def main():
    root = tk.Tk()
    root.geometry('1000x850')
    ticketing_system = TicketingSystem()
    app = App(root, ticketing_system)
              
    root.mainloop()

if __name__ == "__main__":
    main()

