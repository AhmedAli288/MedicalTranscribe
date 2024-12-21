import whisper
import sounddevice as sd
import numpy as np
import tempfile
import wave
import os

# Load the Whisper model
model = whisper.load_model("large-v3")  # Use "tiny", "base", "small", "medium", or "large"

# Function to record audio from the microphone
def record_audio(duration=5, sample_rate=16000, device=None):
    print(f"Recording for {duration} seconds...")
    print(f"Using device: {device}")  # Debugging selected device
    audio = sd.rec(int(duration * sample_rate), 
                   samplerate=sample_rate, 
                   channels=1, 
                   dtype='int16',
                   device=device)  # Specify device in sd.rec
    sd.wait()  # Wait for the recording to finish
    return audio.flatten()

# Save the audio to a temporary WAV file
def save_audio_to_wav(audio, sample_rate):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    try:
        with wave.open(temp_file.name, "wb") as wf:
            wf.setnchannels(1)  # Mono channel
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())
        return temp_file.name
    except Exception as e:
        temp_file.close()
        os.remove(temp_file.name)
        raise e

# Function to continuously listen and transcribe
def continuous_listen_and_transcribe(sample_rate=16000, device=None):
    print("Listening... Say 'end session' to stop.")
    while True:
        # Record short audio clips (e.g., 5 seconds)
        audio_data = record_audio(duration=5, sample_rate=sample_rate, device=device)
        
        # Save the recorded audio to a temporary WAV file
        temp_wav = save_audio_to_wav(audio_data, sample_rate)
        
        try:
            # Transcribe the audio using Whisper
            print("Transcribing...")
            result = model.transcribe(temp_wav)  # Specify English as the language
            transcription = result["text"]
            print("Transcription:", transcription)

            # Check for the "end session" command
            if "end session" in transcription.lower():
                print("Session ended by user.")
                break
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
                print(f"Temporary file {temp_wav} deleted.")

# Main function to set up and start the process
def main():
    sample_rate = 16000  # Whisper expects 16kHz audio

    # List available audio devices
    print("Available audio devices:")
    print(sd.query_devices())  # Prints device list

    # Select input device (Replace index with your desired device index)
    selected_device = 1  # Change this based on your device list

    # Start the continuous listening and transcription process
    continuous_listen_and_transcribe(sample_rate=sample_rate, device=selected_device)

if __name__ == "__main__":
    main()
