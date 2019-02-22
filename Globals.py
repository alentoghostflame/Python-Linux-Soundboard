'''

The file that contains all the storage locations that will be used in between threads.

'''


class GlobalVariables:
    def __init__(self):
        self.input = InputClass()
        self.online = OnlineClass()
        self.file = FileClass()
        self.misc = MiscClass()


class InputClass:
    def __init__(self):
        self.key = 666
        self.page = 1
        self.write_ready = True


class OnlineClass:
    def __init__(self):
        self.main = False
        self.key_detector = False
        self.audio_controller = False
        self.file_controller = False
        self.display_controller = False


class FileClass:
    def __init__(self):
        self.folder_index = []
        self.folder_path_index = []
        self.total_folders = 0
        self.file_index = []
        self.file_path_index = []


class MiscClass:
    def __init__(self):
        self.quit = False
        self.os_detected = 0
        self.event_blocker = True


global_variables = GlobalVariables()





