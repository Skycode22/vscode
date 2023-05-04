import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.utils import platform
from plyer import storagepath
import mimetypes

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/*'


if platform == 'android':
    from jnius import autoclass
    from plyer.platforms.android import permission

Builder.load_string('''
<FileListButton>:
    text: self.path
    on_release: app.root.open_file(self.path)

<FileExplorer>:
    orientation: 'vertical'
    path_input: path_input
    file_list: file_list
    BoxLayout:
        size_hint_y: None
        height: 30
        TextInput:
            id: path_input
            size_hint_x: 85
        Button:
            text: 'Load Files'
            size_hint_x: 15
            on_release: root.get_files()
    RecycleView:
        id: file_list
        viewclass: 'FileListButton'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
''')

class FileListButton(Button, RecycleDataViewBehavior):
    path = StringProperty('')

class FileExplorer(BoxLayout):
    path_input = ObjectProperty()
    file_list = ObjectProperty()

    def __init__(self, **kwargs):
        super(FileExplorer, self).__init__(**kwargs)
        if platform == 'android':
            self.path_input.text = storagepath.get_primary_shared_storage_path()
        else:
            self.path_input.text = os.path.expanduser("~")

    def get_files(self):
        path = self.path_input.text
        if os.path.exists(path):
            files = [{'path': os.path.join(path, f)} for f in os.listdir(path) if not f.startswith('.')]
            self.file_list.data = files
        else:
            popup = Popup(title='Error',
                          content=Label(text='Invalid directory path'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def open_file(self, path):
        print(f"Attempting to open: {path}")
        if os.path.isdir(path):
            self.path_input.text = path
            self.get_files()
        else:
            if platform == 'android':
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')

                intent = Intent()
                intent.setAction(Intent.ACTION_VIEW)
                file = File(path)
                file_uri = Uri.fromFile(file)
                mime_type = get_mime_type(path)
                intent.setDataAndType(file_uri, mime_type)
                intent.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                currentActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                currentActivity.startActivity(intent)
                print(f"Opened file: {path}")
            else:
                # Add functionality to open the file in the appropriate app for other platforms
                pass

class FileExplorerApp(App):
    def build(self):
        if platform == 'android':
            permission.request_permission('android.permission.READ_EXTERNAL_STORAGE')
        return FileExplorer()

if __name__ == '__main__':
    FileExplorerApp().run()
