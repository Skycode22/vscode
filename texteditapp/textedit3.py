import os
import io
import docx
import openpyxl
import pdfplumber

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView


class FileEditor(BoxLayout):
    def __init__(self, **kwargs):
        super(FileEditor, self).__init__(**kwargs)
        self.orientation = "vertical"
        
        # Create UI widgets
        self.file_chooser = FileChooserIconView(path=os.getcwd(), size_hint=(1, 0.8))
        self.file_chooser.filters = ["*.docx", "*.xlsx", "*.pdf"]
        self.file_chooser.bind(on_selection=self.select_file)
        self.edit_button = Button(text="Edit File", size_hint=(1, 0.1))
        self.edit_button.bind(on_press=self.edit_file)

        # Add UI widgets to layout
        self.add_widget(self.file_chooser)
        self.add_widget(self.edit_button)

    def select_file(self, instance, selection):
        if selection:
            self.file_path = selection[0]
            _, extension = os.path.splitext(self.file_path)
            if extension not in [".docx", ".xlsx", ".pdf"]:
                self.show_error_popup("Unsupported file format")
                self.file_path = None
            else:
                print(f"Selected file: {self.file_path}")

    def edit_file(self, instance):
        if hasattr(self, "file_path"):
            print(f"Editing file: {self.file_path}")
            ext = os.path.splitext(self.file_path)[1]
            content = ""
            try:
                if ext == ".docx":
                    doc = docx.Document(self.file_path)
                    for paragraph in doc.paragraphs:
                        content += f"{paragraph.text}\n"
                elif ext == ".xlsx":
                    workbook = openpyxl.load_workbook(self.file_path)
                    worksheet = workbook.active
                    for row in worksheet.iter_rows():
                        content += " | ".join([str(cell.value) for cell in row]) + "\n"
                elif ext == ".pdf":
                    with pdfplumber.open(self.file_path) as pdf:
                        for page in pdf.pages:
                            content += f"{page.extract_text()}\n"
                print(f"File content: {content}")
                self.show_editor_popup(content)
            except Exception as e:
                print(f"Error: {str(e)}")
                self.show_error_popup(str(e))

    def show_editor_popup(self, content):
        popup = Popup(title="Edit Content", size_hint=(0.9, 0.9))
        box = BoxLayout(orientation="vertical")
        text_input = TextInput(text=content, size_hint=(1, 0.9))
        save_button = Button(text="Save", size_hint=(1, 0.1))
        save_button.bind(on_press=popup.dismiss)
        box.add_widget(text_input)
        box.add_widget(save_button)
        popup.content = box
        popup.open()

    def show_error_popup(self, message):
        popup = Popup(title="Error", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class FileEditorApp(App):
    def build(self):
        return FileEditor()


if __name__ == "__main__":
    FileEditorApp().run()