from typing import Optional

import pyaudio


class AudioStream:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.audio_interface = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.PyAudio.Stream] = None

    def __enter__(self):
        self.stream = self.audio_interface.open(*self.args, **self.kwargs)
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.stop_stream()
        self.stream.close()
        self.audio_interface.terminate()
