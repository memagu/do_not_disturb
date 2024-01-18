from pathlib import Path

import pyaudio
from thefuzz import fuzz

from audio.audio_stream import AudioStream
from audio.audio_processing import bytes_to_dbfs, NoiseLevel
from audio.speech_recognition import SpeechRecognizer
from popup import PopupManager

RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK_SIZE = 8000

SPEECH_RECOGNITION_MODEL_PATH = Path("./resources/speech_to_text_models/vosk-model-small-sv-rhasspy-0.15/")

POPUP_TEXT = "Du är för högljudd! Var snäll be om ursäkt. \"Förlåt, jag ska vara tystare\" godtas."
PASSPHRASE = "förlåt jag ska vara tystare"
POPUP_REMOVAL_THRESHOLD = 80


def main() -> None:
    popup_manager = PopupManager()
    speech_recognizer = SpeechRecognizer(SPEECH_RECOGNITION_MODEL_PATH, RATE)

    with (AudioStream(rate=RATE, channels=CHANNELS, format=FORMAT, input=True, frames_per_buffer=CHUNK_SIZE) as stream):
        while True:
            data = stream.read(CHUNK_SIZE)

            if popup_manager.popup_exists:
                spoken_phrase = speech_recognizer.speech_to_text(data)
                print(repr(spoken_phrase))
                if fuzz.ratio(spoken_phrase, PASSPHRASE) >= POPUP_REMOVAL_THRESHOLD:
                    print("Apology detected, removing popup.")
                    popup_manager.destroy_popup()
                continue

            dbfs = bytes_to_dbfs(data)
            noise_level = NoiseLevel.from_dbfs(dbfs)
            print(noise_level)
            if noise_level == NoiseLevel.SCREAMING:
                print("Scream detected, creating popup.")
                popup_manager.create_unclosable(POPUP_TEXT)


if __name__ == '__main__':
    main()
