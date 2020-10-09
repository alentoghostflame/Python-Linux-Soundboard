from soundboard.storage_module import StorageManager
from soundboard.audio_module import AudioManager
from typing import Optional
from threading import Thread
from pathlib import Path
from time import sleep
import subprocess
import logging
import struct
import select


logger = logging.getLogger("soundboard")


# The stuff dealing with this was mostly taken from StackOverflow, and should probably be replaced with something better
# if possible.
JANK_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(JANK_FORMAT)
KEY_CODES = {
    # These are simply Keyboard Key Codes to an integer that the program can use.
    71: 6,
    72: 7,
    73: 8,
    75: 3,
    76: 4,
    77: 5,
    79: 0,
    80: 1,
    81: 2,
}
KEY_NEXT_PAGE = 78  # Numpad Plus Key
KEY_PREV_PAGE = 74  # Numpad Minus Key
KEY_STOP_SOUNDS = 82


class InputManager(Thread):
    def __init__(self, storage: StorageManager, audio: AudioManager):
        Thread.__init__(self)
        self._storage: StorageManager = storage
        self._audio: AudioManager = audio
        # self._gui: Optional[SoundboardWindow] = None
        self._gui = None
        self._should_stop: bool = False
        self._desired_path: Optional[Path] = None
        self._file = None

    def set_event_path(self, path: Path):
        logger.debug(f"Desired path set to {path}")
        self._desired_path = path

    def set_gui(self, gui):
        self._gui = gui

    def stop(self):
        self._should_stop = True

    def run(self) -> None:
        while not self._should_stop:
            self.loop()

    def loop(self):
        if self._desired_path:
            if self._file:
                self._file.close()
            try:
                self._file = open(self._desired_path, "rb")
                logger.debug("Opened desired path.")
            except PermissionError:
                chown_event_file(self._desired_path)
                self._file = open(self._desired_path, "rb")
            except FileNotFoundError:
                logger.warning(f"{self._desired_path} does not exist!")
            finally:
                self._desired_path = None
        if self._file:
            if select.select([self._file], [], [], 2.0)[0]:
                data = self._file.read(EVENT_SIZE)
                (tv_sec, tv_usec, key_type, code, value) = struct.unpack(JANK_FORMAT, data)
                if (key_type != 0 or code != 0) and code != 4 and value == 1:
                    # print("Event type %u, code %u, value %u at %d.%d" % (key_type, code, value, tv_sec, tv_usec))
                    if code == KEY_NEXT_PAGE:
                        self._gui.increment_page()
                    elif code == KEY_PREV_PAGE:
                        self._gui.decrement_page()
                    elif code == KEY_STOP_SOUNDS:
                        self._audio.stop_sounds()
                    else:
                        output_key = KEY_CODES.get(code, -1)
                        if output_key >= 0:
                            self._gui.press_audio_button(output_key)
        else:
            sleep(0.5)


def chown_event_file(event_file_path):
    """
    Takes in the path to an event file that needs to be chown'd, and launches a gnome-terminal with the chown command
    running in it, and awaiting the sudo password of the user if the file exists.
    :param event_file_path: String containing the file path to the event file to be chown'd.
    :return: None
    """
    logger.debug(f"Executing chown on \"{event_file_path}\"")
    command = subprocess.Popen(f"gnome-terminal --window --title=\"Fix Permission of " + event_file_path +
                               "\" --wait -- sudo chown $USER:$USER " + event_file_path, stdout=subprocess.PIPE,
                               shell=True)
    while command.poll() is None:
        sleep(0.5)
