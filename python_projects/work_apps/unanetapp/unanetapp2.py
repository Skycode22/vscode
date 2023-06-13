import webbrowser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class MyApp(App):
    def build(self):
        # create a box layout
        box_layout = BoxLayout(spacing=10, orientation='horizontal')

        # set the background color of the box layout
        with box_layout.canvas.before:
            Color(1, 1, 1, 1) # set the color to white
            self.rect = Rectangle(size=box_layout.size, pos=box_layout.pos)
        box_layout.bind(size=self._update_rect, pos=self._update_rect)

        # create a button with an image
        button = Button(size_hint=(.65, .65), pos_hint={'center_x': 0.5, 'center_y': 0.5}, background_color=(0, 1, 1, 1))
        image = AsyncImage(source='https://seeklogo.com/images/U/unanet-logo-C74B018A7C-seeklogo.com.png')
        button.add_widget(image)
        
        # open the website when the button is clicked
        def on_button_click(instance):
            webbrowser.open('http://unanet.ycg.com/LogOn?ReturnUrl=%2Fmobile')
        button.bind(on_press=on_button_click)

        # add the button to the box layout
        box_layout.add_widget(button)

        return box_layout
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
if __name__ == '__main__':
    MyApp().run()
