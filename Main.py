"""

The main start file for Python Voice Chat Soundboard.
Main.py starts up the threads and tells them to shut down when need be. This is the file that a user should be running.

"""
from time import sleep
import sys
from Globals import global_variables
import Config
from Logger import *
from KeyDetectors import StartKeyDetection
import AudioPlayer
import FileExplorer
import DisplayController
from Dictionaries import OS_DICT


def main():
    '''
    Initialized and runs all the various threads, then sleeps until a KeyboardInturrupt occurs.
    '''
    Config.init()
    global_variables.misc.os_detected = DetectOS()
    global_variables.input.key = 5
    ''' If Windows is detected, enable ANSI escape stuff '''
    if global_variables.misc.os_detected is 3:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    StartKeyDetection()
    while global_variables.misc.event_blocker is True:
        sleep(0.5)
    AudioPlayer.StartAudioController()
    FileExplorer.init()
    FileExplorer.StartFileController()
    DisplayController.StartDisplayController()
    global_variables.online.main = True
    while True:
        sleep(1)


def DetectOS():
    return OS_DICT[sys.platform]


try:
    '''
    The purpose of this try-except is to catch Keyboard Inturrupts and properly close down the threads.
    '''
    main()
except KeyboardInterrupt:
    global_variables.misc.quit = True
    while global_variables.online.key_detector is True or global_variables.online.display_controller is True or \
            global_variables.online.audio_controller is True or global_variables.online.file_controller is True:
        sleep(0.5)
    print("All threads have quit, quitting!")
