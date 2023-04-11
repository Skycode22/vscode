import toga
import webbrowser
import requests
import os
from toga import Image

canvas = toga.Canvas()
box = toga.Box()

def button_handler(widget):
    url = 'http://unanet.ycg.com/LogOn?ReturnUrl=%2Fmobile'
    webbrowser.open_new(url)

def build(app):
    

    button = toga.Button("", on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1

    button.style.color = 'white'
    button.style.font_family = 'arial'
    button.style.width = 540
    button.style.height = 350
    button.style.font_size = 20
    button.style.font_weight = 'bold'

    box.add(button)

    # Download and save the image locally
    response = requests.get('https://upload.wikimedia.org/wikipedia/commons/7/7e/Unanet_Logo.png')
    with open('unanet_logo.png', 'wb') as f:
        f.write(response.content)

    # Create a Toga Image object from the downloaded image file
    image = Image(os.path.abspath('unanet_logo.png'))

    # Set the background image to the Toga Image object
    button.style.background_color = 'white'
    button.style.background_image = image
    button.style.background_size = 'contain'

    return box

def main():
    return toga.App("Unanet", "org.beeware.helloworld", startup=build)

if __name__ == "__main__":
    main().main_loop()
