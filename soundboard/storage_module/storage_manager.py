from soundboard.storage_module.config_manager import SoundboardConfig
from typing import Dict, List, Tuple, Optional
from copy import deepcopy
from pathlib import Path
import logging


SOUND_FILE_EXTENSIONS: Tuple[str, ...] = (".wav", ".ogg")
logger = logging.getLogger("soundboard")


class StorageManager:
    def __init__(self, config: SoundboardConfig):
        self._config: SoundboardConfig = config
        self._root_folder: str = self._config.default_sound_folder

        self._discovered_sounds: Dict[Path, List[Path]] = dict()
        self._mapped_folders: List[Path] = list()
        self._mapped_sounds: Dict[Path, Dict[int, Path]] = dict()

    def reset_sounds(self):
        logger.debug("Resetting discovered folders and sounds.")
        self._discovered_sounds = dict()
        self._mapped_folders = list()
        self._mapped_sounds = dict()

    def discover(self) -> Dict[Path, List[Path]]:
        logger.debug("Discovering sounds.")
        self._discover_folders()
        self._search_folders()
        return self._discovered_sounds

    def map(self):
        logger.debug("Mapping discovered songs.")
        self._map_folders()
        self._map_all_sounds()

    def get_mapped_folders(self) -> List[Path]:
        return self._mapped_folders.copy()

    def get_mapped_sounds(self) -> Dict[Path, Dict[int, Path]]:
        return deepcopy(self._mapped_sounds)

    def get_mapped_sound(self, folder: Path, index: int) -> Optional[Path]:
        if folder in self._mapped_sounds and index in self._mapped_sounds[folder]:
            return self._mapped_sounds[folder][index]
        else:
            return None

    def get_discovered(self) -> Dict[Path, List[Path]]:
        return deepcopy(self._discovered_sounds)

    def get_indexed_sound(self, folder: int, index: int) -> Optional[Path]:
        if 0 <= folder < len(self._mapped_folders) and index in self._mapped_sounds[self._mapped_folders[folder]]:
            return self._mapped_sounds[self._mapped_folders[folder]][index]
        else:
            return None

    def _discover_folders(self):
        root_folder = Path(self._root_folder)
        if root_folder.is_dir():
            for child in root_folder.iterdir():
                if child.is_dir():
                    self._discovered_sounds[child] = list()
                else:
                    logger.debug("Found folder that isn't actually a folder, ignoring.")
        else:
            logger.warning("Given folder to discover isn't a folder, not doing anything.")

    def _search_folders(self):
        for folder in self._discovered_sounds:
            self._discover_sounds(folder)

    def _discover_sounds(self, folder_path: Path):
        for possible_sound in folder_path.iterdir():
            if possible_sound.is_file() and possible_sound.name.endswith(SOUND_FILE_EXTENSIONS):
                self._discovered_sounds[folder_path].append(possible_sound)
            else:
                logger.debug(f"Rejected file {possible_sound}")
        self._discovered_sounds[folder_path].sort()

    def _map_folders(self):
        self._mapped_folders = list(self._discovered_sounds.keys())
        self._mapped_folders.sort()

    def _map_all_sounds(self):
        for folder_path in self._discovered_sounds:
            self._map_sounds(folder_path)

    def _map_sounds(self, folder: Path):
        for sound_path in self._discovered_sounds[folder]:
            for i in range(9):
                if sound_path.name.startswith(f"{i + 1} "):
                    if folder not in self._mapped_sounds:
                        self._mapped_sounds[folder] = dict()
                    self._mapped_sounds[folder][i] = sound_path
                    logger.debug(f"Mapped {folder.name}[{i}] to {sound_path.name}")
                    break
