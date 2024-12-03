from groq import Groq
import speech_to_text

# get your key 
api_key = 'api key goes here' #insert your api key from https://console.groq.com/keys here.

question = f"Give a direct response in few sentences to the question and let your answer be streamed lined to education and academics, and if a non educational or academical question is asked, answer with diplomacy that you can't give response to it, this is the question {speech_to_text.audio_to_text_converter('recording.wav')}"

def talk(Question):
  client = Groq(api_key = api_key)
  completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": Question
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

  # see this part? just take it like that 
  all_words =[]
  for chunk in completion:
      all_words.append((chunk.choices[0].delta.content or ""))
  sentence = ''
  for word in all_words:
    sentence = sentence + word
  return sentence


# Just call the function with your question 
print(talk(question))

def llama_response():
    return talk(question)
