import androidhelper
import datetime
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from gtts import gTTS
import os
import webbrowser
import wikipedia

# Initialize the Androidhelper library
droid = androidhelper.Android()

# Create a KivyMD GUI interface for the assistant
class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Add a label to display the assistant's greeting
        self.greeting_label = Label(text='', size_hint=(1, 0.2))
        self.add_widget(self.greeting_label)

        # Add a text input field for user input
        self.text_input = MDTextField(hint_text="Type your command here")
        self.add_widget(self.text_input)

        # Add a button to capture user input
        self.submit_button = MDRectangleFlatButton(text='Submit', on_press=self.handle_command)
        self.add_widget(self.submit_button)

        # Add a label to display the assistant's responses
        self.response_label = Label(text='', size_hint=(1, 0.6))
        self.add_widget(self.response_label)
        
        

    # Define a method to handle user input
    def handle_command(self, *args):
        command = self.text_input.text

        # Use Androidhelper to capture user input
        droid.ttsSpeak("You said: " + command)

        
        # Check if the user wants to check the battery status
        if 'battery' in command:
            battery_status = droid.batteryGetStatus().result
            battery_percentage = droid.batteryGetLevel().result
            response = "Battery status: {}, Battery percentage: {}".format(battery_status, battery_percentage)

        # Check if the user wants to search for a topic on Wikipedia
        if 'wikipedia' in command:
            # Remove the "wikipedia" keyword from the user's command
            query = command.replace('wikipedia', '').strip()

            try:
                # Search Wikipedia for the topic
                result = wikipedia.summary(query, sentences=2)
                response = "According to Wikipedia, " + result
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle cases where the search query is ambiguous
                options = e.options[:5]
                response = "Your query was ambiguous. Here are some possible options: " + ", ".join(options)
            except wikipedia.exceptions.PageError as e:
                # Handle cases where the search query does not exist on Wikipedia
                response = "Sorry, I could not find any information about " + query + " on Wikipedia."
            except Exception as e:
                # Handle any other errors that may occur
                response = "Sorry, something went wrong while searching for " + query + " on Wikipedia. Please try again."

        # Check if the user wants to open the web browser
        if 'open browser' in command:
            webbrowser.open('https://www.google.com/')
            response = "Opening the web browser"

        # Check if the user wants to close the web browser
        elif 'close browser' in command:
            os.system("pkill chromium")
            response = "Closing the web browser"

        # Use a natural language processing library to understand the user's intent
        # In this example, we'll just repeat the user's command back to them
        else:
            response = "You said: " + command

        # Use text-to-speech to generate a spoken response
        tts = gTTS(text=response, lang='en')
        tts.save('response.mp3')
        os.system('mpg123 response.mp3')

        # Display the assistant's response on the GUI
        self.response_label.text = response

# Create a Kivy App to run the assistant interface
class MyApp(MDApp):
    def build(self):
        # Get the current time of day and greet the user appropriately
        now = datetime.datetime.now()
        if now.hour < 12:
            greeting = "Good morning!"
        elif now.hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        self.root.greeting_label.text = greeting

        # Enter into a loop to continuously ask for the user's command and respond appropriately
        while True:
            command = droid.recognizeSpeech().result
            if command:
                self.root.text_input.text = command
                self.root.handle_command()
            else:
                self.root.response_label.text = "Sorry, I didn't catch that. Please try
                
if __name__ == '__main__':
    MyApp().run()
