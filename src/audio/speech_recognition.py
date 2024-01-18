import json
from pathlib import Path

from vosk import KaldiRecognizer, Model


class SpeechRecognizer:
    def __init__(self, model_path: Path, rate: int = 16000) -> None:
        self.model = Model(str(model_path))
        self.recognizer = KaldiRecognizer(self.model, rate)

        self.rate = rate

    def speech_to_text(self, data: bytes) -> str:
        if self.recognizer.AcceptWaveform(data):
            return json.loads(self.recognizer.Result())["text"]

        return ""
