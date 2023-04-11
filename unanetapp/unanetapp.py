import toga
import webbrowser

def button_handler(widget):
    url = 'https://unanet.com'
    webbrowser.open_new(url)

def build(app):
    box = toga.Box()

    button = toga.Button("Unanet", on_press=button_handler)
    button.style.width = 100
    button.style.height = 50
    button.style.border_width = 0
    button.style.border_bottom_width = 25
    button.style.border_bottom_color = 'green'
    button.style.border_left_width = 13
    button.style.border_left_color = 'transparent'
    button.style.border_right_width = 13
    button.style.border_right_color = 'transparent'
    button.style.border_top_width = 25
    button.style.border_top_color = 'green'
    button.style.color = 'gold'  # Change button text color to gold
    button.style.font_family = 'arial'  # Change font to sans-serif
    box.add(button)
    box.style.background_color = 'lightblue'

    return box

def main():
    return toga.App("First App", "org.beeware.helloworld", startup=build)

if __name__ == "__main__":
    main().main_loop()
