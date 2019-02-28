'''

The file that contains all of the config options available for the user.

'''


class GlobalConfigClass:
    def __init__(self):
        '''
        All the config options for the user to edit as they please. Should not be modified by the program AT ALL.
        '''
        ''' EventFileLocation (STRING DEFAULT: /dev/input/event4) What event file to get keyboard inputs from. '''
        self.event_file_location = "/dev/input/event4"
        ''' DisplayPollingRate (INT DEFAULT: 5) How many times per-second does the Display thread render a new frame to
        the screen. Higher the number, faster the terminal visually updates, but higher the CPU usage. '''
        self.display_polling_rate = 5
        ''' RootSoundFolder (STRING DEFAULT: Sound Files) What the name of the root folder (located next to all the 
        python files) should be. Touching this should not cause issues, and will just change what sound folder is looked 
        into. Good for changing sound packs. '''
        self.root_sound_folder = "Sound Files"
        ''' FilePollingRate (INT DEFAULT: 5) How many times per-second does the FileExplorer thread look for new files 
        and perform actions. Actions include looking for new files, and responding to the numpad + and - keys
        (changing pages). Increasing this will increase CPU usage and Disk IO usage.
        '''
        self.file_polling_rate = 5

        self.use_gui = True

        self.audio = AudioClass()

        ''' Initializes all the config options. User should not edit this '''
        self.display_polling_rate = 1 / self.display_polling_rate
        self.file_polling_rate = 1 / self.file_polling_rate


class AudioClass:
    def __init__(self):
        ''' Audio related user-editable variables. '''

        ''' polling_rate (INT DEFAULT: 1 / 20) How many times per-second does the AudioPlayer check for commands given. 
            Increasing this will increase CPU usage, but make pressing keys to play audio files more responsive. '''
        self.polling_rate = 1 / 20
        ''' max_sound_threads (INT DEFAULT: 10) How many sound threads can be active at one time. Increasing this will
        allow you to have more sounds running concurrently.'''
        self.max_sound_threads = 10
        ''' create_loopback (BOOLEAN DEFAULT: True) If the soundboard should create a loopback so the user can hear the
        audio the soundboard plays.'''
        self.create_loopback = True


global_config = GlobalConfigClass()



