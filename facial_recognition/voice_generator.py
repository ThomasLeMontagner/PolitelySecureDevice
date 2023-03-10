import pyttsx3

class voice_generator():
    def __init__(self):
        # Initialize an engine for voice generator
        self.engine = pyttsx3.init()

    # Greet the person by saying his name
    def greet(self, name):        
        self.engine.say("Hello, {}".format(name))
        self.engine.runAndWait()