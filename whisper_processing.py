import os
from dotenv import load_dotenv
from speech_threading import transcripts


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

client = OpenAI(api_key = api_key)

def audio_processing(audio_name):
    audio_path = f'/Users/majdalsehnawi/Library/Mobile Documents/com~apple~CloudDocs/Reed/_Freshman_Year/Personal Projects/fact-checker/output/{audio_name}.wav'

    audio_file = open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    #Delete the temp audio path
    if os.path.exists(audio_path):
        os.remove(audio_path)

    #Adds the transcript for processing
    transcripts.append(transcription)


