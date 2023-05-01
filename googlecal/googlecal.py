import datetime
import os.path
import tkinter as tk
from tkinter import messagebox
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/tasks']
def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
def get_events(creds):
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])
def get_tasks(creds):
    service = build('tasks', 'v1', credentials=creds)
    tasks_result = service.tasks().list(tasklist='@default').execute()
    return tasks_result.get('items', [])
def save_events(creds, updated_events):
    service = build('calendar', 'v3', credentials=creds)
    for event in updated_events:
        try:
            updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print(f"Updated: {updated_event['summary']} ({updated_event['start']['dateTime']})")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    return True
def save_tasks(creds, updated_tasks):
    service = build('tasks', 'v1', credentials=creds)
    for task in updated_tasks:
        try:
            updated_task = service.tasks().update(tasklist='@default', task=task['id'], body=task).execute()
            print(f"Updated: {updated_task['title']}")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    return True
def update_events_and_tasks():
    updated_events = []
    for i, event in enumerate(events):
        summary = event_text_widgets[i].get("1.0", "end-1c")
        if summary != event['summary']:
            event['summary'] = summary
            updated_events.append(event)
    updated_tasks = []
    for i, task in enumerate(tasks):
        title = task_text_widgets[i].get("1.0", "end-1c")
        if title != task['title']:
            task['title'] = title
            updated_tasks.append(task)
    if save_events(credentials, updated_events) and save_tasks(credentials, updated_tasks):
        messagebox.showinfo("Success", "Events and tasks updated successfully!")
    else:
        messagebox.showerror("Error", "An error occurred while updating events and tasks.")
credentials = get_credentials()
events = get_events(credentials)
tasks = get_tasks(credentials)
root = tk.Tk()
root.title("Google Calendar Events and Tasks")
frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
content_frame = tk.Frame(frame, bg="white")
content_frame.pack(fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(content_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas = tk.Canvas(content_frame, bg="white", yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=canvas.yview)
inner_frame = tk.Frame(canvas, bg="white")
canvas.create_window(0, 0, window=inner_frame, anchor='nw')
event_text_widgets = []
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    start_time = datetime.datetime.fromisoformat(start).strftime("%m/%d/%Y %I:%M %p")
    event_text = f"{start_time} - {event['summary']}"
    text_widget = tk.Text(inner_frame, height=1, wrap=tk.WORD)
    text_widget.insert(tk.END, event_text)
    text_widget.pack(fill=tk.X, expand=True, pady=5)
    event_text_widgets.append(text_widget)
task_label = tk.Label(inner_frame, text="Tasks:", bg="white", font=("Arial", 12, "bold"))
task_label.pack(pady=(10, 0))
task_text_widgets = []
for task in tasks:
    task_text = task['title']
    text_widget = tk.Text(inner_frame, height=1, wrap=tk.WORD)
    text_widget.insert(tk.END, task_text)
    text_widget.pack(fill=tk.X, expand=True, pady=5)
    task_text_widgets.append(text_widget)
inner_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))
save_button = tk.Button(frame, text="Save Changes", command=update_events_and_tasks)
save_button.pack(pady=10)
root.mainloop()

