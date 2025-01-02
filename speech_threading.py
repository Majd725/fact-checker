import pyaudio
import threading
import wave
from chatgpt_processing import fact_checking
#Transcription Storage
transcripts = []


# Constants for audio recording
RATE = 16000  # Sampling rate
CHUNK = 1024  # Number of audio frames per buffer
CHUNKS_PER_20_SECONDS = int((RATE * 20) / CHUNK)  # Chunks needed for 20 seconds

# Array to store audio data in real time
audio_stream_data = []

# Lock for thread-safe access to the audio data
lock = threading.Lock()

def record_audio():
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,  # 16-bit format
        channels=1,             # Mono audio
        rate=RATE,              # Sampling rate
        input=True,             # Set as input
        frames_per_buffer=CHUNK # Buffer size
    )

    print("Recording started...")

    try:
        while True:
            # Read a chunk of audio data
            audio_data = audio_stream.read(CHUNK, exception_on_overflow=False)

            # Append audio data to the array in a thread-safe manner
            with lock:
                audio_stream_data.append(audio_data)
    except KeyboardInterrupt:
        print("Recording stopped.")
    finally:
        # Cleanup
        audio_stream.stop_stream()
        audio_stream.close()
        audio_interface.terminate()


#Save the audio to file to send to Whisper API
def save_to_file(file_name, seg):
    audio_interface = pyaudio.PyAudio()
    with wave.open(file_name, "wb") as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(audio_interface.get_sample_size(pyaudio.paInt16))  # 16-bit samples
        wf.setframerate(RATE)  # Sampling rate
        wf.writeframes(b"".join(seg))  # Combine chunks and write


def process_audio():
    """Process the audio data in 20-second segments."""
    print("Processing started...")
    buffer = []  # Temporary buffer to store 20 seconds of audio
    while True:
        with lock:
            if audio_stream_data:
                # Transfer available chunks to the buffer
                buffer.extend(audio_stream_data)
                audio_stream_data.clear()

        # Check if the buffer has 20 seconds of data
        if len(buffer) >= CHUNKS_PER_20_SECONDS:
            # Extract 20 seconds of audio
            segment = buffer[:CHUNKS_PER_20_SECONDS]
            buffer = buffer[CHUNKS_PER_20_SECONDS:]  # Remove processed data

            file_namer = 1 #Counter for file name
            save_to_file(f'audio_{file_namer}',segment)
            file_namer+=1
            processing_thread = threading.Thread(target=process_audio(), args=f'audio_{file_namer-1}')
            processing_thread.start()
        if (len(transcripts)!=0):

            gptoutput = fact_checking()
            #Check if the 20 sec had anything incorrect
            if gptoutput!='.':
                print("MISTAKE")
                print(gptoutput)


if __name__ == "__main__":
    # Start the recording thread
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()
    # Start processing audio in the main thread
    try:
        process_audio()
    except KeyboardInterrupt:
        print("Stopping...")
        recording_thread.join()
