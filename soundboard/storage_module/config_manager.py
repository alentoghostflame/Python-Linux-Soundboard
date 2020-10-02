import pathlib
import logging
import yaml


logger = logging.getLogger("soundboard")


class BaseConfig:
    @classmethod
    def __init_subclass__(cls, name: str = "default_config_name", **kwargs):
        super().__init_subclass__(**kwargs)
        cls._config_name = name
        cls._from_disk = False

    def _to_dict(self) -> dict:
        output_dict = dict()
        for key in self.__dict__:
            if key[0] != "_":
                output_dict[key] = self.__dict__[key]
        return output_dict

    def save(self):
        logger.debug("Saving config file.")
        file_name = f"{self._config_name}.yaml"
        file = open(file_name, "w")
        yaml.safe_dump(self._to_dict(), file)
        file.close()

    def _from_dict(self, state: dict):
        for key in state:
            if key in self.__dict__:
                self.__dict__[key] = state[key]

    def load(self):
        file_name = f"{self._config_name}.yaml"
        if pathlib.Path(file_name).is_file():
            logger.debug("Found config, loading.")
            file = open(file_name, "r")
            state = yaml.safe_load(file)
            file.close()
            self._from_dict(state)
            self._from_disk = True
        else:
            logger.debug("No config found, using default values.")

    def from_disk(self) -> bool:
        return self._from_disk


class SoundboardConfig(BaseConfig, name="soundboard_config"):
    def __init__(self):
        self.max_sounds: int = 10
        self.default_sound_folder: str = "Sound Files"
