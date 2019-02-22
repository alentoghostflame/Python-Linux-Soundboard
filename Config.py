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
        ''' SoundPollingRate (INT DEFAULT: 20) How many times per-second does the AudioPlayer check for commands given. 
        Increasing this will increase CPU usage. '''
        self.audio_polling_rate = 20

        self.use_gui = False

        ''' Initializes all the config options. User should not edit this '''
        self.display_polling_rate = 1 / self.display_polling_rate
        self.file_polling_rate = 1 / self.file_polling_rate
        self.audio_polling_rate = 1 / self.audio_polling_rate


global_config = GlobalConfigClass()



