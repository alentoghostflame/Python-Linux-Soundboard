from soundboard.storage_module import SoundboardConfig, StorageManager
from openal import oalOpen, oalQuit
from openal import Source as OALSource, AL_STOPPED
from pathlib import Path
from typing import List, Optional
import logging


logger = logging.getLogger("soundboard")


class AudioManager:
    def __init__(self, config: SoundboardConfig, storage: StorageManager):
        self._config: SoundboardConfig = config
        self._storage: StorageManager = storage
        self._audio_threads: List[OALSource] = list()

    def get_audio_count(self) -> int:
        self.clean_sounds()
        return len(self._audio_threads)

    def play_sound(self, file_path: Path):
        logger.debug(f"Playing sound at {file_path}")
        openal_thread = oalOpen(str(file_path))
        self._audio_threads.append(openal_thread)
        openal_thread.play()

    def stop_sounds(self):
        for openal_thread in self._audio_threads:
            openal_thread.stop()
        self.clean_sounds()

    def clean_sounds(self):
        for thread in self._audio_threads.copy():
            if thread.get_state() == AL_STOPPED:
                self._audio_threads.remove(thread)

    def exit(self):
        oalQuit()
