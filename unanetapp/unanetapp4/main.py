#Import the necessary modules
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
import webbrowser
from kivy.core.window import Window
from kivy.uix.label import Label

#Set the background color
Window.clearcolor = (.5, 1, 1, 1)

#Create a button with an image
class ImageButton(ButtonBehavior, AsyncImage):
    def on_press(self):
        url = "http://unanet.ycg.com/LogOn?ReturnUrl=%2Fmobile"
        webbrowser.open(url)

#Create a box layout with a button and label
class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        icon = 'unanet_logo.png'
        button_box = BoxLayout(orientation='vertical')
        button = ImageButton(source=icon, size_hint=(0.5, 0.5))
        button_box.add_widget(button)
        label = Label(text="Enter your own text here", font_size=30)
        button_box.add_widget(label)
        self.add_widget(button_box)

#Create the app
class Test(App):
    def build(self):
        return MainWindow()

#Run the app
if __name__ == "__main__":
    Test().run()
