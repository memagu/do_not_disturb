from audio.audio_stream import AudioStream
from audio.audio_processing import bytes_to_dbfs, NoiseLevel
from audio.constants import CHANNELS, CHUNK_SIZE, FORMAT, RATE


def main() -> None:
    with AudioStream(rate=RATE, channels=CHANNELS, format=FORMAT, input=True, frames_per_buffer=CHUNK_SIZE) as stream:
        while True:
            data = stream.read(CHUNK_SIZE)
            dbfs = bytes_to_dbfs(data)
            noise_level = NoiseLevel.from_dbfs(dbfs)

            match noise_level:
                case NoiseLevel.BACKGROUND_NOISE:
                    print("background noise")
                case NoiseLevel.SPEAKING:
                    print("speaking")
                case NoiseLevel.SPEAKING_LOUDLY:
                    print("speaking loudly")
                case NoiseLevel.SCREAMING:
                    print("screaming")
                case _:
                    raise Exception(f"Undefined NoiseLevel: {noise_level}")


if __name__ == '__main__':
    main()
