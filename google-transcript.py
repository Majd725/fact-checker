import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


from openai import OpenAI

client = OpenAI(api_key = api_key)


audio_file = open(
             "/Users/majdalsehnawi/Library/Mobile Documents/com~apple~CloudDocs/Reed/_Freshman_Year/Personal Projects/fact-checker/output/audio_1.wav"
    , "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
)

print(transcription)

