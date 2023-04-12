import toga
import webbrowser
import requests
import os
from toga import Image

box = toga.Box()

def button_handler(widget):
    url = 'http://unanet.ycg.com/LogOn?ReturnUrl=%2Fmobile'
    webbrowser.open_new(url)

def build(app):
    # Download and save the image locally
    response = requests.get('https://seeklogo.com/images/U/unanet-logo-C74B018A7C-seeklogo.com.png')
    with open('unanet_logo.png', 'wb') as f:
        f.write(response.content)
    image = Image('unanet_logo.png')
    button = toga.Button("", on_press=button_handler)
    button.image = image
    button.style.padding = 50
    button.style.width = 540
    button.style.height = 350
    box.add(button)
    return box

def main():
    return toga.App("Unanet", "org.beeware.helloworld", startup=build)

if __name__ == "__main__":
    main().main_loop()
