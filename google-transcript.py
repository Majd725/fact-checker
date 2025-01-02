from openai import OpenAI

client = OpenAI()


audio_file = open(
             "/Users/majdalsehnawi/Library/Mobile Documents/com~apple~CloudDocs/Reed/_Freshman_Year/Personal Projects/fact-checker/output/audio_1.wav"
    , "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
)


