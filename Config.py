'''

The file that contains all of the config options available for the user.

'''


class ConfigOptions:
    '''
    All the config options for the user to edit as they please.
    '''
    ''' EventFileLocation (STRING DEFAULT: /dev/input/event4) What event file to get keyboard inputs from. '''
    EventFileLocation = "/dev/input/event4"
    ''' DisplayPollingRate (INT DEFAULT: 5) How many times per-second does the Display thread render a new frame to the
    screen. Higher the number, faster the terminal visually updates, but higher the CPU usage. '''
    DisplayPollingRate = 5
    ''' RootSoundFolder (STRING DEFAULT: Sound Files) What the name of the root folder (located next to all the python
     files) should be. Touching this should not cause issues, and will just change what sound folder is looked into.
     Good for changing sound packs. '''
    RootSoundFolder = "Sound Files"
    ''' FilePollingRate (INT DEFAULT: 5) How many times per-second does the FileExplorer thread look for new files and
    perform actions. Actions include looking for new files, and responding to the numpad + and - keys (changing pages).
    Increasing this will increase CPU usage and Disk IO usage.
    '''
    FilePollingRate = 5
    ''' SoundPollingRate (INT DEFAULT: 20) How many times per-second does the AudioPlayer check for commands given. 
    Increasing this will increase CPU usage. '''
    AudioPollingRate = 20




def init():
    ''' Initializes all the config options. Main.py should be calling this. User should not edit this '''
    global Config
    Config = ConfigOptions
    Config.DisplayPollingRate = 1 / Config.DisplayPollingRate
    Config.FilePollingRate = 1 / Config.FilePollingRate
    Config.AudioPollingRate = 1 / Config.AudioPollingRate




