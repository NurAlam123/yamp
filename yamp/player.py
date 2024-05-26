import requests
from io import BytesIO
from pydub import AudioSegment
from threading import Thread, Event
from time import sleep
import numpy as np
import sounddevice as sd
import math

from yamp.utils import time_formatter


class Player:
    "The Media Player"

    def __init__(self) -> None:
        self.audio_segment: AudioSegment = None
        self.audio = b""
        self.audio_player: Thread = None

        self.is_playing = False
        self.is_paused = False
        self.stop_thread: Event = Event()

        self.current_frame_position = 0
        self.current_position = 0
        self.total_duration = 0

        self.sleep_time = 0.5

        self.volume = 0.5

    def reset(self):
        self.__init__()

    def play_audio(self, url: str) -> None:
        self.reset()

        # res = requests.get(url)
        # self.audio = music_file = BytesIO(res.content)
        # self.audio_segment = AudioSegment.from_file(music_file)
        self.audio = url
        self.audio_segment = AudioSegment.from_file(url)[50000:]
        self.total_duration = math.floor(self.audio_segment.duration_seconds)

        self.audio_player = Thread(target=self._play, daemon=True)
        self.audio_player.start()
        return 1

    # the main play function
    def _play(self) -> None:
        self.is_playing = True

        audio_data = np.array(self.audio_segment.get_array_of_samples())
        sample_rate = self.audio_segment.frame_rate
        channels = self.audio_segment.channels

        def callback(out_data: np.ndarray, frames: int, time, status):
            if self.stop_thread.is_set():
                # slow down the pause so that doesn't make unexpected sound
                sleep(self.sleep_time)
                return
            start = self.current_frame_position
            end = start + frames * channels
            out_data[:] = (
                (audio_data[start:end] * self.volume)
                .astype(np.int16)
                .reshape(out_data.shape)
            )
            self.current_frame_position = end

        with sd.OutputStream(
            callback=callback, channels=channels, samplerate=sample_rate, dtype="int16"
        ):
            while self.is_playing and not self.stop_thread.is_set():
                self.current_position += self.sleep_time
                if self.current_position >= self.total_duration:
                    self.stop_thread.set()
                    break
                sleep(self.sleep_time)

    def pause(self) -> int:
        # if there is thread available and the thread is running then stop it
        if self.audio_player:
            if self.audio_player.is_alive():
                self.stop_thread.set()
        self.is_paused = True
        self.is_playing = False
        return 1

    def resume(self) -> int:
        current_position = self.current_position * 1000
        # slice the audio from the current position to perfectly resume form the left off
        self.audio_segment = AudioSegment.from_file(self.audio)[current_position:]
        # again start the player
        self.audio_player = Thread(target=self._play, daemon=True)
        self.stop_thread.clear()
        self.is_paused = False
        self.is_playing = True
        self.current_frame_position = 0
        self.audio_player.start()
        return 1

    def stop(self) -> int:
        if not self.stop_thread.is_set():
            self.stop_thread.set()

        self.stop_thread.clear()
        self.__init__()

    def status(self) -> str:
        if not self.is_playing and not self.is_paused:
            return "00:00/00:00"

        total_duration_format = time_formatter(self.total_duration)
        current_position_format = time_formatter(math.floor(self.current_position))

        return f"{current_position_format}/{total_duration_format}"
