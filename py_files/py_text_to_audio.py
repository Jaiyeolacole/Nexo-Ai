import pyttsx3
import llama
import time
import audio_com_to_esp


def save_audio():

    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties if needed (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    # Text to save as speech
    text = f"Hi my name is nexo, {llama.llama_response()}"

    # Save the speech to a WAV file
    output_file = "output.wav"
    engine.save_to_file(text, output_file)

    # Run the engine to generate and save the speech
    engine.runAndWait()

    print(f"Audio saved as {output_file}")
    return True
    
if __name__ == '__main__':
    save_audio()
    time.sleep(1)
    audio_com_to_esp.send_file('C:/Users/SERGPC1/Desktop/Nexoai/py_files/output.wav', '192.168.137.100', 8080)