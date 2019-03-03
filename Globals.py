import configparser as cp
from os.path import isfile
from Logger import log, INFO  # , WARNING, ERROR
'''

The file that contains all the storage locations that will be used in between threads.

'''


class GlobalVariablesClass:
    '''
    Used for easy communication between threads throughout the soundboard.
    input: See InputClass.
    online: See OnlineClass.
    file: See FileClass.
    misc: See MiscClass.
    '''
    def __init__(self):
        self.input = self.InputClass()
        self.online = self.OnlineClass()
        self.file = self.FileClass()
        self.audio = self.AudioClass()
        self.misc = self.MiscClass()

    class InputClass:
        '''
        Holds information about input.
        key: Integer representing the last key pressed, written to by the key_detector, read by the file_controller
        and audio_controller.
        page: Integer representing what page/folder the user wants to play sounds from, written to and read from by
        the file_controller
        write_ready: Holds a boolean representing what last wrote or read from key. If write_ready is True, that means that
        the file_controller or audio_controller has processed key, and key_detector cannot write a new key. If write_ready
        is False, that means key_detector can write a new value to key, and file_controller and audio_controller cannot read
        key.
        '''
        def __init__(self):
            self.key = 666
            self.page = 0
            self.write_ready = True
            self.event_file = global_config.audio.event_file_location

    class OnlineClass:
        '''
        Holds information concerning the status of the threads.
        main: Boolean representing if main is online or not.
        key_detector: Boolean representing if the key_detector is online or not.
        audio_controller: Boolean representing if the audio_controller is online or not.
        file_controller: Boolean representing if the file_controller is online or not.
        display_controller: Boolean representing if the display_controller is online or not.
        '''
        def __init__(self):
            self.main = False
            self.key_detector = False
            self.input_controller = False
            self.audio_controller = False
            self.file_controller = False
            self.display_controller = False

    class FileClass:
        '''
        Holds information concerning the file system.
        '''
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
        '''
        Miscellaneous variables that don't quite fit in the above categories, or need a category of their own.
        quit: Boolean that represents if the program should quit or not. Written to by main, read by all threads.
        os_detected: Integer that represents what operating system the host is running. See Dictionaries.OS_DICT for values,
        event_blocker: Boolean the key_detector uses to delay main until the key_detector is online.
        '''
        def __init__(self):
            self.quit = False
            self.os_detected = 0
            self.key_detection_started = False


class GlobalConfigClass:
    def __init__(self):
        self.file_config = cp.ConfigParser()
        if isfile("Config.ini") is False:
            self.file_config["MAIN"] = {"use_gui": "True"}
            self.file_config["AUDIO"] = {"root_sound_folder": "Sound Files", "polling_rate": "1 / 20",
                                         "max_audio_threads": "10", "event_file_location": "None", "create_loopback": "True"}
            self.file_config["INPUT"] = {"polling_rate": "1 / 20"}
            with open("Config.ini", "w") as configfile:
                self.file_config.write(configfile)
        else:
            self.file_config.read("Config.ini")

        self.main = self.MainClass(self.file_config)
        self.audio = self.AudioClass(self.file_config)
        self.input = self.InputClass(self.file_config)

    class MainClass:
        def __init__(self, file_config):
            self.use_gui = eval(process_config_value(file_config, "MAIN", "use_gui", "True"))

    class AudioClass:
        def __init__(self, file_config):
            self.root_sound_folder = str(process_config_value(file_config, "AUDIO", "root_sound_folder", "Sound Files"))
            self.polling_rate = eval(process_config_value(file_config, "AUDIO", "polling_rate", 1 / 20))

            self.max_audio_threads = int(process_config_value(file_config, "AUDIO", "max_audio_threads", 10))
            self.event_file_location = str(process_config_value(file_config, "AUDIO", "event_file_location", "None"))
            if self.event_file_location == "None":
                self.event_file_location = None
            else:
                pass
            self.create_loopback = eval(process_config_value(file_config, "AUDIO", "create_loopback", "True"))

    class InputClass:
        def __init__(self, file_config):
            self.polling_rate = eval(process_config_value(file_config, "INPUT", "polling_rate", 1 / 20))


def process_config_value(file_config, input_category, input_variable, input_fallback):
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





