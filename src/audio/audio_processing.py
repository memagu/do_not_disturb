from __future__ import annotations

from enum import Enum
import math

import numpy as np


class NoiseLevel(Enum):
    BACKGROUND_NOISE = 0
    SPEAKING = 1
    SPEAKING_LOUDLY = 2
    SCREAMING = 3

    @classmethod
    def from_dbfs(cls, dbfs: float) -> NoiseLevel:
        if dbfs <= -40:
            return cls.BACKGROUND_NOISE
        elif dbfs <= -20:
            return cls.SPEAKING
        elif dbfs <= -10:
            return cls.SPEAKING_LOUDLY
        else:
            return cls.SCREAMING


def rms(data: np.ndarray) -> float:
    assert data.ndim == 1, "Data array must be 1-dimensional"

    return np.sqrt(np.mean(np.square(data)))


def rms_to_dbfs(rms_value: float, reference: float = 32768) -> float:
    return 20 * math.log10(rms_value / reference)


def bytes_to_dbfs(data: bytes) -> float:
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    return rms_to_dbfs(rms(audio_data))
