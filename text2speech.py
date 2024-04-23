import os
import dotenv
import playsound
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

dotenv.load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)


def text_to_speech(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="elhZ9FDhAnPXWy3WhtFg",  # Eve voice ID
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2",  # use `eleven_multilingual_v2` for other languages (higher latency)
        voice_settings=VoiceSettings(
            stability=0.35,
            similarity_boost=0.1,
            style=0.0,
            use_speaker_boost=False,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    # Playing the voice
    playsound.playsound(save_file_path, True)

    # Promptly deleting the file after playing not to take space in the storage
    os.remove(save_file_path)

    return save_file_path
