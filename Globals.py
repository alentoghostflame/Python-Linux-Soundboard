from Config import global_config
'''

The file that contains all the storage locations that will be used in between threads.

'''


class GlobalVariables:
    '''
    Used for easy communication between threads throughout the soundboard.
    input: See InputClass.
    online: See OnlineClass.
    file: See FileClass.
    misc: See MiscClass.
    '''
    def __init__(self):
        self.input = InputClass()
        self.online = OnlineClass()
        self.file = FileClass()
        self.audio = AudioClass()
        self.misc = MiscClass()


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
        self.event_file = global_config.event_file_location


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
    folder_index: List of strings representing names of folders
    folder_path_index: List of strings representing paths of folders.
    total_folders: Integer representing the number of folders.
    file_index: List of strings representing names of files.
    file_path_index: List of strings representing paths of files.
    '''
    def __init__(self):
        self.folder_index = []
        self.folder_path_index = []
        self.total_folders = 0
        self.file_index = []
        self.file_path_index = []

        # NEW STUFF
        # folder_names: A list of strings whose index value corresponds to the folder name's number prefix.
        self.folder_names = []
        # file_names: A list of strings whose index value corresponds to the file name's number prefix.
        self.file_names = []
        # file_paths: A list of lists of strings. Each string is a path to a file. Each list's index number corresponds
        # to the folder name's number prefix that the file is inside of.
        self.file_paths = []
        # locked: Tracks if the values above are being changed or not, and if they should be read or not.
        self.locked = False


class AudioClass:
    def __init__(self):
        self.thread_count = 0
        self.kill_audio = False


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
        self.event_blocker = True



global_variables = GlobalVariables()





