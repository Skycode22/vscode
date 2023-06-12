import sqlite3
from tkinter import *
from tkinter import messagebox

def create_database():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            description TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def submit_ticket(description):
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("INSERT INTO tickets (description, status) VALUES (?, 'Open')", (description,))
    conn.commit()
    conn.close()

def view_tickets():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tickets WHERE status='Open'")
    rows = c.fetchall()
    conn.close()
    return rows

def resolve_ticket(id):
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("UPDATE tickets SET status = 'Resolved' WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def main():
    create_database()
    root = Tk()
    root.geometry("300x200")

    def open_admin_console():
        admin_root = Toplevel(root)
        admin_root.geometry("400x400")

        listbox = Listbox(admin_root)
        listbox.pack()

        def view_tickets_callback():
            tickets = view_tickets()
            listbox.delete(0, END)
            for ticket in tickets:
                text = f"ID: {ticket[0]}, Description: {ticket[1]}, Status: {ticket[2]}"
                listbox.insert(END, text)

        def resolve_ticket_callback():
            if listbox.curselection():
                selected_ticket = listbox.get(ACTIVE)
                if selected_ticket:
                    try:
                        ticket_id = int(selected_ticket.split(",")[0].split(":")[1].strip())
                        resolve_ticket(ticket_id)
                        view_tickets_callback()
                        messagebox.showinfo("Success", f"Ticket {ticket_id} has been resolved.")
                    except ValueError:
                        messagebox.showerror("Error", "Invalid ticket ID.")
                else:
                    messagebox.showwarning("No ticket selected", "Please select a ticket before trying to resolve.")
            else:
                messagebox.showwarning("No ticket selected", "Please select a ticket before trying to resolve.")

        Button(admin_root, text="View Tickets", command=view_tickets_callback).pack()
        Button(admin_root, text="Resolve Selected Ticket", command=resolve_ticket_callback).pack()

    def open_user_console():
        user_root = Toplevel(root)
        user_root.geometry("300x200")

        def submit_ticket_callback():
            description = input_entry.get()
            submit_ticket(description)
            messagebox.showinfo("Success", "Your ticket has been submitted.")

        input_entry = Entry(user_root)
        input_entry.pack()
        Button(user_root, text="Submit Ticket", command=submit_ticket_callback).pack()

    Button(root, text="Open Admin Console", command=open_admin_console).pack()
    Button(root, text="Open User Console", command=open_user_console).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
