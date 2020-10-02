import configparser as cp
from os.path import isfile
from bad_old.logger import log, INFO  # , WARNING, ERROR
'''

The file that contains all the storage locations that will be used in between threads.

'''


class GlobalVariablesClass:
    """
    Used for easy communication of variables between threads (if need be) without passing through insane amounts of
    variables.
    """
    def __init__(self):
        self.input = self.InputClass()
        self.online = self.OnlineClass()
        self.file = self.FileClass()
        self.audio = self.AudioClass()
        self.misc = self.MiscClass()

    class InputClass:
        """
        page: Integer, holds the current index value for file.file_names and file.file_paths.
        event_file_location: Holds either a string that is a path to a file, or None to indicate that there is no path.
        key_detection_started: True if key detection is running, False if not.
        """
        def __init__(self):
            self.page = 0
            self.event_file_location = global_config.input.event_file_location
            self.key_detection_started = False

    class OnlineClass:
        """
        Holds information on the status of threads.
        If True, than the thread is alive and ready.
        False, its off or not ready.
        """
        def __init__(self):
            self.main = False
            self.key_detector = False

    class FileClass:
        """
        Holds information concerning the file system.
        """
        def __init__(self):

            # folder_names: A list of strings whose index value corresponds to the folder name's number prefix.
            self.folder_names = []
            # file_names: A list of strings whose index value corresponds to the file name's number prefix.
            self.file_names = []
            # file_paths: A list of lists of strings. Each string is a path to a file. Each list's index number
            # corresponds to the folder name's number prefix that the file is inside of.
            self.file_paths = []
            # locked: Tracks if the values above are being changed or not, and if they should be read or not.
            self.locked = False

    class AudioClass:
        def __init__(self):
            self.thread_count = 0
            self.kill_audio = False
            self.null_sink = 0
            self.loopback = 0

    class MiscClass:
        """
        Miscellaneous variables that don't quite fit in the above categories, or need a category of their own.
        quit: Boolean that represents if the program should quit or not. Written to by main, read by all threads.
        """
        def __init__(self):
            self.quit = False


class GlobalConfigClass:
    """
    Reads config.ini and creates a globally accessible class file that has the relevant parameters and values specified
    by config.ini
    If a required parameter is missing from config.ini, use a default value.
    If config.ini is missing, create a new one and use default values for everything.
    """
    def __init__(self):
        self.file_config = cp.ConfigParser()
        if isfile("config.ini") is False:
            # If config.ini is missing, create a new one.
            log(INFO, "GlobalConfigClass", "config.ini missing, creating a new one.")
            self.file_config["MAIN"] = {"use_gui": "True"}
            self.file_config["AUDIO"] = {"root_sound_folder": "Sound Files", "polling_rate": "1 / 20",
                                         "max_audio_threads": "10", "create_loopback": "True"}
            self.file_config["INPUT"] = {"event_file_location": "None"}
            with open("config.ini", "w") as configfile:
                self.file_config.write(configfile)
        else:
            log(INFO, "GlobalConfigClass", "Reading config.ini")
            self.file_config.read("config.ini")

        self.main = self.MainClass(self.file_config)
        self.audio = self.AudioClass(self.file_config)
        self.input = self.InputClass(self.file_config)

    class MainClass:
        def __init__(self, file_config):
            self.use_gui = eval(process_config_value(file_config, "MAIN", "use_gui", "True"))

    class AudioClass:
        def __init__(self, file_config):
            self.root_sound_folder = str(process_config_value(file_config, "AUDIO", "root_sound_folder", "Sound Files"))
            self.polling_rate = eval(process_config_value(file_config, "AUDIO", "polling_rate", "1 / 20"))
            self.max_audio_threads = int(process_config_value(file_config, "AUDIO", "max_audio_threads", "10"))
            self.create_loopback = eval(process_config_value(file_config, "AUDIO", "create_loopback", "True"))

    class InputClass:
        def __init__(self, file_config):
            self.event_file_location = str(process_config_value(file_config, "INPUT", "event_file_location", "None"))
            if self.event_file_location == "None":
                self.event_file_location = None
            else:
                pass


def process_config_value(file_config, input_category, input_variable, input_fallback):
    """
    Attempt to read the config option specified with the variables and return it. If the config option is missing,
    return the fallback instead.
    :param file_config: The dictionary given by ConfigParser.
    :param input_category: The overall category that the config option is in, ex [MAIN]
    :param input_variable: The config option that is attempting to be read, ex use_gui
    :param input_fallback: The fallback option that will be used if the config option is missing, ex True
    :return: Either the value of the config option, or the value of input_fallback.
    """
    if input_category in file_config and input_variable in file_config[input_category]:
        output = file_config[input_category][input_variable]
        log(INFO, "process_config_value", "Config value [" + input_category + "](" + input_variable + ") read as \"" +
            str(output) + "\"")
    else:
        output = input_fallback
        log(INFO, "process_config_value", "Config value [" + input_category + "](" + input_variable +
            ") missing, defaulting to \"" + str(output) + "\"")
    return output


global_config = GlobalConfigClass()


global_variables = GlobalVariablesClass()





