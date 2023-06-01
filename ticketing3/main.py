import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog

# Database setup
conn = sqlite3.connect('tickets.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tickets
             (id integer primary key, title text, description text, status text, priority integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS archived_tickets
             (id integer primary key, title text, description text, status text, priority integer)''')

# GUI setup
root = Tk()
root.geometry('800x800')

view_frame = Frame(root, highlightbackground="black", highlightthickness=1)
view_frame.pack(pady=10)

archived_frame = Frame(root, highlightbackground="black", highlightthickness=1)
archived_frame.pack(pady=10)

def create_ticket():
    title = title_entry.get()
    description = description_entry.get('1.0', 'end-1c')  # Get the text from the Text widget
    priority = int(priority_entry.get())
    c.execute("INSERT INTO tickets (title, description, status, priority) VALUES (?, ?, 'Open', ?)", (title, description, priority,))
    conn.commit()
    messagebox.showinfo('Success', 'Ticket created successfully!')
    view_tickets()  # Refresh the view

def edit_ticket(id):
    # Fetch existing ticket details
    c.execute("SELECT * FROM tickets WHERE id = ?", (id,))
    ticket = c.fetchone()

    # Create a new window to edit the ticket
    edit_window = Toplevel(root)
    edit_window.title(f"Edit Ticket #{id}")

    Label(edit_window, text='Title').pack()
    title_entry = Entry(edit_window)
    title_entry.insert(0, ticket[1])  # Pre-fill with existing title
    title_entry.pack()

    Label(edit_window, text='Description').pack()
    description_entry = Text(edit_window, height=4, width=50)
    description_entry.insert('1.0', ticket[2])  # Pre-fill with existing description
    description_entry.pack()

    Label(edit_window, text='Priority (1-5)').pack()
    priority_entry = Entry(edit_window)
    priority_entry.insert(0, ticket[4])  # Pre-fill with existing priority
    priority_entry.pack()

    Button(edit_window, text='Save', command=lambda: save_ticket(id, title_entry.get(), description_entry.get('1.0', 'end-1c'), int(priority_entry.get()))).pack()

def save_ticket(id, title, description, priority):
    # Update the ticket details in the database
    c.execute("UPDATE tickets SET title = ?, description = ?, priority = ? WHERE id = ?", (title, description, priority, id,))
    conn.commit()
    view_tickets()  # Refresh the view

def delete_ticket(id):
    c.execute("DELETE FROM tickets WHERE id = ?", (id,))
    conn.commit()
    view_tickets()  # Refresh the view

def archive_ticket(id):
    # Fetch the ticket details
    c.execute("SELECT * FROM tickets WHERE id = ?", (id,))
    ticket = c.fetchone()

    # Insert the ticket into the archived tickets table
    c.execute("INSERT INTO archived_tickets (id, title, description, status, priority) VALUES (?, ?, ?, ?, ?)",
              (ticket[0], ticket[1], ticket[2], ticket[3], ticket[4]))
    conn.commit()

    # Delete the ticket from the main tickets table
    c.execute("DELETE FROM tickets WHERE id = ?", (id,))
    conn.commit()

    view_tickets()  # Refresh the view

def delete_archived_ticket(id):
    c.execute("DELETE FROM archived_tickets WHERE id = ?", (id,))
    conn.commit()
    view_archived_tickets()  # Refresh the view

def view_tickets():
    for widget in view_frame.winfo_children():
        widget.destroy()  # Clear all existing widgets in view_frame

    Label(view_frame, text='View Tickets').pack()

    c.execute('SELECT * FROM tickets')
    rows = c.fetchall()
    for row_index, row in enumerate(rows):
        ticket_frame = Frame(view_frame, highlightbackground="black", highlightthickness=1)
        ticket_frame.pack(pady=10)

        Label(ticket_frame, text=f"ID: {row[0]}").pack()
        Label(ticket_frame, text=f"Title: {row[1]}").pack()
        Label(ticket_frame, text=f"Description: {row[2]}").pack()
        Label(ticket_frame, text=f"Status: {row[3]}").pack()
        Label(ticket_frame, text=f"Priority: {row[4]}").pack()

        Button(ticket_frame, text='Edit', command=lambda id=row[0]: edit_ticket(id)).pack(side=LEFT)
        Button(ticket_frame, text='Delete', command=lambda id=row[0]: delete_ticket(id)).pack(side=LEFT)
        Button(ticket_frame, text='Archive', command=lambda id=row[0]: archive_ticket(id)).pack(side=LEFT)

def view_archived_tickets():
    for widget in archived_frame.winfo_children():
        widget.destroy()  # Clear all existing widgets in archived_frame

    Label(archived_frame, text='Archived Tickets').pack()

    c.execute('SELECT * FROM archived_tickets')
    rows = c.fetchall()
    for row_index, row in enumerate(rows):
        ticket_frame = Frame(archived_frame, highlightbackground="black", highlightthickness=1)
        ticket_frame.pack(pady=10)

        Label(ticket_frame, text=f"ID: {row[0]}").pack()
        Label(ticket_frame, text=f"Title: {row[1]}").pack()
        Label(ticket_frame, text=f"Description: {row[2]}").pack()
        Label(ticket_frame, text=f"Status: {row[3]}").pack()
        Label(ticket_frame, text=f"Priority: {row[4]}").pack()

        Button(ticket_frame, text='Delete', command=lambda id=row[0]: delete_archived_ticket(id)).pack(side=LEFT)

def switch_to_view_tickets():
    view_frame.pack(pady=10)
    archived_frame.pack_forget()
    view_tickets()

def switch_to_view_archived_tickets():
    archived_frame.pack(pady=10)
    view_frame.pack_forget()
    view_archived_tickets()

# Create ticket section
create_frame = Frame(root, highlightbackground="black", highlightthickness=1)
create_frame.pack(pady=10)

Label(create_frame, text='Create Ticket').pack()
title_label = Label(create_frame, text='Title')
title_label.pack()
title_entry = Entry(create_frame)
title_entry.pack()
description_label = Label(create_frame, text='Description')
description_label.pack()
description_entry = Text(create_frame, height=4, width=50)
description_entry.pack()
priority_label = Label(create_frame, text='Priority (1-5)')
priority_label.pack()
priority_entry = Entry(create_frame)
priority_entry.pack()
Button(create_frame, text='Submit Ticket', command=create_ticket).pack()

# Bind Enter key to Submit Ticket button
root.bind('<Return>', lambda event: create_ticket())

# View tickets section
Button(root, text='View Tickets', command=switch_to_view_tickets).pack()
Button(root, text='View Archived Tickets', command=switch_to_view_archived_tickets).pack()

root.mainloop()
conn.close()
