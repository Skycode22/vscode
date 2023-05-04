from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from smb_script import get_files

class FileList(BoxLayout):
    def __init__(self, files, **kwargs):
        super(FileList, self).__init__(**kwargs)
        self.orientation = 'vertical'

        for file in files:
            self.add_widget(Label(text=file))

class MainApp(App):
    def build(self):
        # Replace these with the appropriate values for your environment
        server = '192.168.254.4'
        username = 'skyler.thuss'
        password = '1234YCG!'
        share_name = 'ycg-nas'
        directory = 'Shared'

        files = get_files(server, username, password, share_name, directory)
        file_list = FileList(files)

        scroll_view = ScrollView()
        scroll_view.add_widget(file_list)

        return scroll_view

if __name__ == '__main__':
    MainApp().run()
