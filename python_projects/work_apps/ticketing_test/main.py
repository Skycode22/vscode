import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

# Connect to the database
conn = sqlite3.connect('issues.db')
cursor = conn.cursor()

# Create issues table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_text TEXT,
        date TEXT,
        status TEXT DEFAULT 'Open'
    )
''')
conn.commit()

# Function to submit an issue
def submit_issue():
    issue_text = issue_entry.get()
    if issue_text:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO issues (issue_text, date) VALUES (?, ?)", (issue_text, date))
        conn.commit()
        messagebox.showinfo('Success', 'Issue submitted successfully.')
        issue_entry.delete(0, tk.END)
        display_open_issues()
    else:
        messagebox.showwarning('Error', 'Please enter an issue.')

# Function to display open issues
def display_open_issues():
    cursor.execute("SELECT * FROM issues WHERE status = 'Open'")
    open_issues = cursor.fetchall()
    issue_list.delete(0, tk.END)
    for issue in open_issues:
        issue_id = issue[0]
        issue_text = issue[1]
        date = issue[2]
        status = issue[3]
        issue_list.insert(tk.END, f'#{issue_id}: {date} - {issue_text} ({status})')

# Function to display archived issues
def display_archived_issues(archived_list):
    cursor.execute("SELECT * FROM issues WHERE status = 'Archived'")
    archived_issues = cursor.fetchall()
    archived_list.delete(0, tk.END)
    for issue in archived_issues:
        issue_id = issue[0]
        issue_text = issue[1]
        date = issue[2]
        status = issue[3]
        archived_list.insert(tk.END, f'#{issue_id}: {date} - {issue_text} ({status})')

# Function to edit an issue
def edit_issue():
    selected_index = issue_list.curselection()
    if selected_index:
        selected_issue = issue_list.get(selected_index)
        issue_id = selected_issue.split(':')[0].strip('#')
        new_text = issue_entry.get()
        if new_text:
            cursor.execute("UPDATE issues SET issue_text = ? WHERE id = ?", (new_text, issue_id))
            conn.commit()
            messagebox.showinfo('Success', 'Issue updated successfully.')
            issue_entry.delete(0, tk.END)
            display_open_issues()
        else:
            messagebox.showwarning('Error', 'Please enter a new issue text.')
    else:
        messagebox.showwarning('Error', 'Please select an issue to edit.')

# Function to archive an issue
def archive_issue():
    selected_index = issue_list.curselection()
    if selected_index:
        selected_issue = issue_list.get(selected_index)
        issue_id = selected_issue.split(':')[0].strip('#')
        cursor.execute("UPDATE issues SET status = 'Archived' WHERE id = ?", (issue_id,))
        conn.commit()
        messagebox.showinfo('Success', 'Issue archived successfully.')
        display_open_issues()
    else:
        messagebox.showwarning('Error', 'Please select an issue to archive.')

# Function to delete an issue
def delete_issue():
    selected_index = issue_list.curselection()
    if selected_index:
        selected_issue = issue_list.get(selected_index)
        issue_id = selected_issue.split(':')[0].strip('#')
        confirmation = messagebox.askyesno('Confirmation', 'Are you sure you want to delete this issue?')
        if confirmation:
            cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
            conn.commit()
            messagebox.showinfo('Success', 'Issue deleted successfully.')
            display_open_issues()
    else:
        messagebox.showwarning('Error', 'Please select an issue to delete.')

# Function to open the archived issues window
def open_archived_issues_window():
    archived_window = tk.Toplevel(window)
    archived_window.title('Archived Issues')

    archived_list = tk.Listbox(archived_window, width=50)
    archived_list.pack()

    # Display archived issues
    display_archived_issues(archived_list)

# Create the main window
window = tk.Tk()
window.title('Issue Tracker')

# Set the window background image
bg_image = tk.PhotoImage(file='bg1.png')
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create GUI components for open issues
open_frame = tk.Frame(window)
open_frame.pack(pady=10)

open_label = tk.Label(open_frame, text='Open Issues', bg='lightblue')
open_label.pack()

issue_label = tk.Label(open_frame, text='Enter Issue:', bg='lightblue')
issue_label.pack()

issue_entry = tk.Entry(open_frame, width=50)
issue_entry.pack()

submit_button = tk.Button(open_frame, text='Submit', command=submit_issue, bg='lightblue')
submit_button.pack()

issue_list = tk.Listbox(open_frame, width=50)
issue_list.pack()

edit_button = tk.Button(open_frame, text='Edit', command=edit_issue, bg='lightblue')
edit_button.pack()

archive_button = tk.Button(open_frame, text='Archive', command=archive_issue, bg='lightblue')
archive_button.pack()

delete_button = tk.Button(open_frame, text='Delete', command=delete_issue, bg='lightblue')
delete_button.pack()

# Create GUI components for archived issues
archived_frame = tk.Frame(window)
archived_frame.pack(pady=10)

archived_label = tk.Label(archived_frame, text='Archived Issues', bg='lightblue')
archived_label.pack()

archived_button = tk.Button(archived_frame, text='View Archived Issues', command=open_archived_issues_window, bg='lightblue')
archived_button.pack()

# Display the open issues
display_open_issues()

# Start the main event loop
window.mainloop()

# Close the database connection when the window is closed
conn.close()
