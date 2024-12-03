import pyttsx3


import llama

engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-10)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.say('Hi my name is Nexo.')
engine.say(llama.llama_response())

engine.runAndWait()