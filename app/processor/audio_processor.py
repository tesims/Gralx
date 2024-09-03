import os
import bmf
import requests
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
from config import Config
from app.processor.text_processor import mask_text


# Set up OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AudioProcessor:
    def __init__(self):
        self.openvoice_endpoint_url = "https://9wqe954kukprc0-8000.proxy.runpod.net"

    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using OpenAI's Whisper API."""
        with open(audio_file_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcription.text

    def upload_voice_sample(self, audio_file_path: str) -> str:
        """Upload a voice sample to OpenVoice and return the voice ID."""
        with open(audio_file_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {"audio_file_label": os.path.basename(audio_file_path)}
            response = requests.post(
                f"{self.openvoice_endpoint_url}/upload_audio/",
                files=files,
                data=data
            )
        response.raise_for_status()
        return response.json()["audio_file_label"]

    def clone_voice(self, text: str, voice_id: str) -> bytes:
        """Clone voice using OpenVoice API."""
        params = {
            "text": text,
            "voice": voice_id,
            "accent": "en-newest",
            "speed": 1.0
        }
        response = requests.get(f"{self.openvoice_endpoint_url}/synthesize_speech/", params=params)
        response.raise_for_status()
        return response.content

def process_audio_file(file_path: str, project_description: str) -> Dict:
    """Process an audio file (MP3, WAV, etc.) using BMF and the AudioProcessor."""
    audio_processor = AudioProcessor()

    # Transcribe the full audio
    transcription = audio_processor.transcribe_audio(file_path)

    # Process transcription (mask PII)
    masked_transcription = mask_text(transcription, Config.OPENAI_API_KEY, project_description, "gpt-3.5-turbo")

    # Upload the original audio as a voice sample
    voice_id = audio_processor.upload_voice_sample(file_path)

    # Clone voice with masked transcription
    cloned_audio = audio_processor.clone_voice(masked_transcription, voice_id)

    return {
        'original_transcription': transcription,
        'masked_transcription': masked_transcription,
        'cloned_audio': cloned_audio
    }

def process_multiple_files(file_paths: List[str], project_description: str) -> Dict[str, Dict]:
    """Process multiple audio files."""
    results = {}
    for file_path in file_paths:
        results[file_path] = process_audio_file(file_path, project_description)
    return results

# Test functions
def test_transcribe_audio():
    processor = AudioProcessor()
    transcription = processor.transcribe_audio("/Users/academics/Documents/graxl/graxl-2/app/uploads/test_audio1.mp3")
    print(f"Transcription: {transcription}")

def test_process_audio_file():
    result = process_audio_file("/Users/academics/Documents/graxl/graxl-2/app/uploads/test_audio1.mp3", "This is a test project for audio processing.")
    print(f"Original transcription: {result['original_transcription'][:50]}...")
    print(f"Masked transcription: {result['masked_transcription'][:50]}...")
    print(f"Cloned audio size: {len(result['cloned_audio'])} bytes")

def test_process_multiple_files():
    file_paths = ["/Users/academics/Documents/graxl/graxl-2/app/uploads/test_audio1.mp3", "/Users/academics/Documents/graxl/graxl-2/app/uploads/test_audio2.mp3"]
    results = process_multiple_files(file_paths, "This is a test project for processing multiple audio files.")
    for file_path, result in results.items():
        print(f"File: {file_path}")
        print(f"Original transcription: {result['original_transcription'][:50]}...")
        print(f"Masked transcription: {result['masked_transcription'][:50]}...")
        print(f"Cloned audio size: {len(result['cloned_audio'])} bytes")

if __name__ == "__main__":
    print("Testing transcribe_audio:")
    test_transcribe_audio()

    print("\nTesting process_audio_file:")
    test_process_audio_file()

    print("\nTesting process_multiple_files:")
    test_process_multiple_files()