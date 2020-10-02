from soundboard.storage_module import SoundboardConfig, StorageManager
from soundboard.gui_module import SoundboardWindow
from soundboard.audio_module import AudioManager
import logging
import sys
import os

LOGGING_FORMAT = "[{asctime}][{filename}][{lineno:3}][{funcName}][{levelname}] {message}"
LOGGING_LEVEL = logging.DEBUG


def setup_logging():
    setup_logger = logging.getLogger("soundboard")
    log_format = logging.Formatter(LOGGING_FORMAT, style="{")

    os.makedirs("logs", exist_ok=True)
    log_latest_handler = logging.FileHandler("logs/Soundboard Latest.log", mode="w")

    log_latest_handler.setFormatter(log_format)
    log_console_handler = logging.StreamHandler(sys.stdout)
    log_console_handler.setFormatter(log_format)

    setup_logger.addHandler(log_latest_handler)
    setup_logger.addHandler(log_console_handler)

    setup_logger.setLevel(LOGGING_LEVEL)


logger = logging.getLogger("soundboard")


class PythonSoundboard:
    def __init__(self):
        self._config = SoundboardConfig()
        self._storage: StorageManager = StorageManager(self._config)
        self.audio: AudioManager = AudioManager(self._config, self._storage)
        self._sb_window: SoundboardWindow = SoundboardWindow(self._storage, self.audio)

    def setup(self):
        setup_logging()
        self._config.load()
        self._storage.discover()
        # logger.debug(f"Discovered:\n{self._storage.discover()}")
        self._storage.map()
        # logger.debug(f"Mapped Folders:\n{self._storage.get_mapped_folders()}")
        # logger.debug(f"Mapped Sounds:\n{self._storage.get_mapped_sounds()}")
        self._sb_window.setup()

    def run(self):
        self._sb_window.run()

    def save(self):
        self.audio.exit()
        self._config.save()
