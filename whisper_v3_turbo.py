import requests

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer hf_your_api_key"}  # Replace with your Hugging Face token

# Function to send audio to the Hugging Face model and get transcription
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()  # Read the audio file as binary data
    response = requests.post(API_URL, headers=headers, data=data)  # Send POST request
    return response.json()  # Return the JSON response

# Main function to test the transcription
if __name__ == "__main__":
    # Replace with the path to your audio file
    filename = "medical_sample.m4a"
    
    print("Sending audio file to Hugging Face Whisper model...")
    output = query(filename)  # Call the query function
    
    print("Transcription Output:")
    print(output)  # Print the transcription
