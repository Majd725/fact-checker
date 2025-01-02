import os
from dotenv import load_dotenv

from speech_threading import transcripts

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

client = OpenAI(api_key = api_key)


def fact_checking():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content":
                """This is a conversation between two people. You are going to fact check it. 
                If there isn't anything incorrect say '.' and '.' only dont say anything else. 
                If there is something incorrect say what it is and where you got it from.
                Be sure to distinguish from normal speech and factual speech.
                If it is anything other than incorrect knowledge, reply with a dot '.' """
             },
            {
                "role": "user",
                "content": transcripts[0]
            }
        ]
    )
    return completion

