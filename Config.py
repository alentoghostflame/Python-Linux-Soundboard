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
        ''' RootSoundFolder (STRING DEFAULT: Sound Files) What the name of the root folder (located next to all the 
        python files) should be. Touching this should not cause issues, and will just change what sound folder is looked 
        into. Good for changing sound packs. '''
        self.root_sound_folder = "Sound Files"

        self.use_gui = True

        self.audio = AudioClass()

        self.input = InputClass()


class AudioClass:
    def __init__(self):
        ''' Audio related user-editable variables. '''

        ''' polling_rate (INT DEFAULT: 1 / 20) How many times per-second does the AudioPlayer if an audio thread is done
        playing audio. Increasing this will increase CPU usage, but make killing audio threads more responsive. '''
        self.polling_rate = 1 / 20
        ''' max_sound_threads (INT DEFAULT: 10) How many sound threads can be active at one time. Increasing this will
        allow you to have more sounds running concurrently.'''
        self.max_sound_threads = 10
        ''' create_loopback (BOOLEAN DEFAULT: True) If the soundboard should create a loopback so the user can hear the
        audio the soundboard plays.'''
        self.create_loopback = True


class InputClass:
    def __init__(self):
        """ Input related user-editable variables. """

        ''' polling_rate (FLOAT DEFAULT: 1 / 20) Minimum time the program will wait between ticks before the 
        InputController  will check for any inputs. Increasing this may increase responsiveness of button presses, but
        may increase CPU usage. Setting this to "1 / 20" will cause the InputController to check a maximum of 20 times
        per second (20 ticks per second [20 TPS])'''
        self.polling_rate = 1 / 20


global_config = GlobalConfigClass()



