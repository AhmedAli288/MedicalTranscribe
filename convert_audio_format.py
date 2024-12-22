from pydub import AudioSegment

def convert_to_wav(input_file, output_file):
    try:
        # Load the input audio file and convert to WAV format
        audio = AudioSegment.from_file(input_file, format="m4a")
        audio = audio.set_channels(1)  # Convert to mono channel
        audio = audio.set_frame_rate(16000)  # Resample to 16 kHz
        audio.export(output_file, format="wav")
        print(f"File converted to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
