import requests
import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
import time

# Replace with your AssemblyAI API key
API_KEY = "your_assemblyai_api_key"

HEADERS = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

# Function to record audio in chunks
def record_audio_chunk(duration=5, sample_rate=16000):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    return audio.flatten()

# Save the audio chunk to a temporary WAV file
def save_audio_to_wav(audio, sample_rate):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file.name, "wb") as wf:
        wf.setnchannels(1)  # Mono channel
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    return temp_file.name

# Upload the audio file to AssemblyAI
def upload_audio_to_assemblyai(file_path):
    print("Uploading audio to AssemblyAI...")
    with open(file_path, "rb") as audio_file:
        upload_response = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers=HEADERS,
            data=audio_file
        )
    upload_response.raise_for_status()
    return upload_response.json()["upload_url"]

# Transcribe audio using AssemblyAI
def transcribe_audio(audio_url):
    print("Requesting transcription...")
    transcript_request = {
        "audio_url": audio_url,
        "language_code": "en_us"  # Specify the language
    }
    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        json=transcript_request,
        headers=HEADERS
    )
    transcript_response.raise_for_status()
    transcript_id = transcript_response.json()["id"]

    # Poll for transcription result
    print("Processing transcription...")
    while True:
        result = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=HEADERS
        )
        result_json = result.json()

        if result_json["status"] == "completed":
            return result_json["text"]
        elif result_json["status"] == "failed":
            raise Exception("Transcription failed.")
        time.sleep(2)  # Wait before polling again

# Continuous listening and transcription
def continuous_listen_and_transcribe(sample_rate=16000):
    print("Listening... Say 'end session' to stop.")
    while True:
        # Record a chunk of audio
        audio_data = record_audio_chunk(duration=5, sample_rate=sample_rate)

        # Save the chunk to a temporary WAV file
        temp_wav_file = save_audio_to_wav(audio_data, sample_rate)

        try:
            # Upload the audio to AssemblyAI
            audio_url = upload_audio_to_assemblyai(temp_wav_file)

            # Transcribe the uploaded audio
            transcription = transcribe_audio(audio_url)
            print("Transcription:", transcription)

            # Check for the "end session" command
            if "end session" in transcription.lower():
                print("Session ended by user.")
                break
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_wav_file):
                os.remove(temp_wav_file)
                print(f"Temporary file {temp_wav_file} deleted.")

# Main function to start the process
def main():
    sample_rate = 16000  # AssemblyAI expects 16kHz audio
    continuous_listen_and_transcribe(sample_rate=sample_rate)

if __name__ == "__main__":
    main()
