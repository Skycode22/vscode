import openai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')

openai.api_key = "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"

class MainLayout(BoxLayout):
    topic_input = ObjectProperty()
    language_spinner = ObjectProperty()
    code_output = ObjectProperty()

    def generate_code(self):
        topic = self.topic_input.text.strip()
        language_name = self.language_spinner.text
        prompt = f"Generate a {language_name} code about {topic}"
        model = "text-davinci-003"
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=2500)
        code = response.choices[0].text.strip()
        self.code_output.text = code

    def copy_to_clipboard(self):
        selected_text = self.code_output.selection_text
        if selected_text:
            Clipboard.copy(selected_text)

class RandomCodeGeneratorApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    RandomCodeGeneratorApp().run()
