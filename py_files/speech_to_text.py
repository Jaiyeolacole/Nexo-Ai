# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
import audio_esp_to_com

# Replace with your API key
aai.settings.api_key = "**********************" #your assemblyai api key goes here.
    
  
def audio_to_text_converter(file_url):
    while audio_esp_to_com.main() == False:
        #Do nothing
        continue
    
    else:
    
        FILE_URL = file_url # URL of the file to transcribe

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(FILE_URL)
    
        if transcript.status == aai.TranscriptStatus.error:
            print(transcript.error)
        else:
            print(transcript.text) ## plan on removing this line
            return transcript.text
    
