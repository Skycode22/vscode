import toga
import webbrowser
import requests

def button_handler(widget):
    url = 'https://unanet.com'
    webbrowser.open_new(url)

def build(app):
    box = toga.Box()

    button = toga.Button("Unanet", on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    button.style.background_color = 'green'  # Change button color to blue
    button.style.color = 'gold'  # Change button text color to white
    button.style.font_family = 'arial'  # Change font to sans-serif
    box.add(button)
    box.style.background_color = 'lightblue'

    return box

def main():
    return toga.App("First App", "org.beeware.helloworld", startup=build)

if __name__ == "__main__":
    main().main_loop()