import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import subprocess
import sys
import os

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image(source='delete.gif')
        self.progress = ProgressBar(max=100)
        self.percent_label = Label(text="0%")
        self.text_label = Label(text="Deleting files and directories on server(s) 192.168.254.*")

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.progress)
        self.layout.add_widget(self.percent_label)
        self.layout.add_widget(self.text_label)

        Clock.schedule_interval(self.update_progress, 1)

        return self.layout

    def update_progress(self, dt):
        if self.progress.value < 100:
            self.progress.value += 1
            self.percent_label.text = f'{self.progress.value}%'

    def on_stop(self):
        global restart
        restart = True

def run_app():
    global restart
    restart = False
    MyApp().run()
    if restart:
        os.execl(sys.executable, 'python', __file__)

if __name__ == '__main__':
    run_app()
