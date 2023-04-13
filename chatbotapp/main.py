import openai
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

# Set up the OpenAI API key
openai.api_key = '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'

# Define the chatbot app
class ChatbotApp(App):
    # Define the user input box
    user_input = ObjectProperty(None)

    # Define the chatbot response box
    chatbot_response = ObjectProperty(None)

    def build(self):
        # Set up the GUI layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Add the user input box
        user_input_box = BoxLayout(size_hint=(1, 0.15))
        self.user_input = TextInput(text='', multiline=False, size_hint=(1, None), height=50, halign='center')
        self.user_input.bind(on_text_validate=self.on_enter)  # Bind the on_text_validate event to on_enter method
        user_input_box.add_widget(self.user_input)
        layout.add_widget(user_input_box)

        # Add the chatbot response box
        chatbot_response_box = BoxLayout(size_hint=(1, 0.85))
        self.chatbot_response = Label(text='', size_hint=(1, None), halign='center', valign='top')
        self.chatbot_response.bind(size=self.chatbot_response.setter('text_size'))
        self.chatbot_response.height = Window.height * 0.85 - 50 - 20 - 2 # Height of chatbot response box is the remaining space
        chatbot_response_box.add_widget(self.chatbot_response)
        layout.add_widget(chatbot_response_box)

        return layout

    def on_enter(self, *args):
        # Get the user input
        user_input_text = self.user_input.text

        # Use OpenAI API to generate chatbot response
        prompt = f"User: {user_input_text}\nChatbot:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            temperature=0.7,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Update the chatbot response box with the generated response
        self.chatbot_response.text = response.choices[0].text

# Run the chatbot app
if __name__ == '__main__':
    ChatbotApp().run()
