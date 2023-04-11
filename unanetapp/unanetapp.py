import toga
import webbrowser

def button_handler(widget):
    url = 'https://unanet.com'
    webbrowser.open_new(url)

def build(app):
    box = toga.Box()

    button = toga.Button("Unanet", on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    button.style.background_color = 'lightgreen'  
    button.style.color = 'black'
    button.style.font_family = 'arial'
    button.style.border_radius = 50  # Set border radius to create hexagon shape
    button.style.width = 100
    button.style.height = 100
    box.add(button)
    box.style.background_color = 'blue'

    return box

def main():
    return toga.App("First App", "org.beeware.helloworld", startup=build)

if __name__ == "__main__":
    main().main_loop()
