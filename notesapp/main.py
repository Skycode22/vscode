from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout
import re
Window.size = (1440, 640)
Builder.load_string("""
<NoteTaker>:
    orientation: 'vertical'
    spacing: 5
    TextInput:
        id: input_text
        size_hint_y: None
        height: 40
        multiline: True
    ScrollView:
        GridLayout:
            id: notes_layout
            cols: 2
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
            padding: 5
    BoxLayout:
        size_hint_y: None
        height: 40
        spacing: 5
        Button:
            text: 'Add Image'
            on_press: root.show_image_popup()
<ImagePopup>:
    title: 'Select Image'
    BoxLayout:
        orientation: 'vertical'
        FileChooserIconView:
            id: file_chooser
            filters: ['*.jpg', '*.jpeg', '*.png', '*.gif']
            on_submit: root.load_image(args[1])
        Button:
            text: 'Load Selected Image'
            on_press: root.load_image(file_chooser.selection)
""")
class NoteTaker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_down=self.check_key_combination)
    def check_key_combination(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'shift' and 'ctrl' in modifiers:
            self.add_note()
    def add_note(self):
        text = self.ids.input_text.text
        if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
            note = Button(text=text, size_hint_y=None, height=40, on_press=lambda x: self.open_url(text))
        else:
            note = TextInput(text=text, size_hint_y=None, height=40)
        self.ids.notes_layout.add_widget(note)
        self.ids.input_text.text = ''
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
    def show_image_popup(self):
        popup = ImagePopup()
        popup.open()
    def add_image(self, image_path):
        image = AsyncImage(source=image_path, size_hint_y=None, height=200)
        self.ids.notes_layout.add_widget(image)
class ImagePopup(Popup):
    def load_image(self, selection):
        if selection:
            self.dismiss()
            app = App.get_running_app()
            app.root.add_image(selection[0])
class NoteItem(BoxLayout):
    def delete_item(self):
        parent_layout = self.parent
        parent_layout.remove_widget(self)            
class NoteTakerApp(App):
    def build(self):
        return NoteTaker()
if __name__ == '__main__':
    NoteTakerApp().run()
