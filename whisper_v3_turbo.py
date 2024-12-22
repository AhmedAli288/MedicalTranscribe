import requests
from convert_audio_format import convert_to_wav
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables from the .env file
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"

if not API_URL or not API_KEY:
    raise ValueError("API_URL and API_KEY must be set in the .env file.")

headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to send audio to the Hugging Face model and get transcription
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()  # Read the audio file as binary data
    response = requests.post(API_URL, headers=headers, data=data)  # Send POST request

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response Text: {response.text}")
        return None

    try:
        return response.json()  # Return the JSON response
    except requests.exceptions.JSONDecodeError:
        print("Error: Failed to decode JSON from the response.")
        print(f"Raw Response: {response.text}")
        return None

# Main function to test the transcription
if __name__ == "__main__":
    # Input file (original .m4a) and converted file (.wav)
    input_file = "medical_sample.m4a"
    converted_file = "converted_audio.wav"

    # Convert audio format to .wav
    print("Converting audio format...")
    converted_file = convert_to_wav(input_file, converted_file)

    if converted_file:
        print("Sending audio file to Hugging Face Whisper model...")
        output = query(converted_file)  # Call the query function

        print("Transcription Output:")
        print(output)
