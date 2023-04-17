import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from docx import Document
from openpyxl import load_workbook

class TextEditor(toga.App):
    def startup(self):
        # Create a main window
        self.main_window = toga.MainWindow(title=self.name)

        # Create a text area widget
        self.text_area = toga.MultilineTextInput()

        # Create a save button widget
        self.save_button = toga.Button('Save', on_press=self.save_file)

        # Create an open button widget
        self.open_button = toga.Button('Open', on_press=self.open_file)

        # Create a horizontal box to hold the text area and buttons
        box = toga.Box(children=[self.text_area, self.save_button, self.open_button], style=Pack(direction=ROW))

        # Add the box widget to the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def save_file(self, widget):
        # Get the text from the text area widget
        text = self.text_area.value

        # Open a file dialog to choose a file to save
        file_dialog = self.main_window.save_file_dialog()

        # Determine the file type based on the file extension
        file_extension = file_dialog.file_path.split('.')[-1]

        # Write the text to the file
        if file_extension == 'txt':
            with open(file_dialog.file_path, 'w') as f:
                f.write(text)
        elif file_extension == 'docx':
            document = Document()
            document.add_paragraph(text)
            document.save(file_dialog.file_path)
        elif file_extension == 'xlsx':
            wb = load_workbook(filename=file_dialog.file_path)
            ws = wb.active
            ws['A1'] = text
            wb.save(file_dialog.file_path)

    def open_file(self, widget):
        # Open a file dialog to choose a file to open
        file_dialog = self.main_window.open_file_dialog(title="Open File")
        
        if file_dialog:  # Check if a file is selected
            # Determine the file type based on the file extension
            file_extension = file_dialog[0].split('.')[-1]

            # Read the contents of the file
            if file_extension == 'txt':
                with open(file_dialog[0], 'r') as f:
                    text = f.read()
            elif file_extension == 'docx':
                document = Document(file_dialog[0])
                text = '\n'.join([p.text for p in document.paragraphs])
            elif file_extension == 'xlsx':
                wb = load_workbook(filename=file_dialog[0])
                ws = wb.active
                text = str(ws['A1'].value)

            # Set the text area widget value to the contents of the file
            self.text_area.value = text


def main():
    return TextEditor('Text Editor', 'com.example.texteditor')


if __name__ == '__main__':
    main().main_loop()