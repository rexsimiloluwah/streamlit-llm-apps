import os

from dotenv import load_dotenv, find_dotenv
from elevenlabs import generate, play, save, voices, Voice, VoiceSettings, set_api_key

_ = load_dotenv(find_dotenv())

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
set_api_key(ELEVENLABS_API_KEY)

voice = Voice(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    settings=VoiceSettings(
        stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True
    ),
)

if __name__ == "__main__":
    audio = generate(text="Hello World. My name is Similoluwa Okunowo", voice=voice)

    # Play the audio
    play(audio)

    # Save the audio to a file
    # save(audio, "audio.mp3")
