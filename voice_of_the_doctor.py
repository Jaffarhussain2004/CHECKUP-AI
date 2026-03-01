# voice_of_the_doctor.py

import os
import platform
import subprocess
from dotenv import load_dotenv
from gtts import gTTS
from elevenlabs import ElevenLabs

# Load all API keys from .env file
load_dotenv()

# Get API keys
ELEVENLABS_API_KEY = os.environ.get("ELEVEN_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")   # safe to keep

# -----------------------------
# Google TTS function
# -----------------------------
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    # Auto-play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
    except Exception as e:
        print(f"Error playing audio: {e}")

# -----------------------------
# ElevenLabs TTS function
# -----------------------------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # Generate audio (bytes)
    audio = client.generate(
        text=input_text,
        voice="Aria",                 
        model="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )

    # Save to file
    with open(output_filepath, "wb") as f:
        f.write(audio)

    # Auto-play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
    except Exception as e:
        print(f"Error playing audio: {e}")

# -----------------------------
# Optional test calls
# -----------------------------
if __name__ == "__main__":
    text_to_speech_with_gtts("Hello, this is Google TTS speaking!", "gtts_test.mp3")
    text_to_speech_with_elevenlabs("Hello, I am Dr. Hassan!", "doctor_voice.mp3")
