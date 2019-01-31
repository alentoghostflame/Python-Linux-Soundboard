"""

The main start file for Python Voice Chat Soundboard.
Main.py starts up the threads and tells them to shut down when need be. This is the file that a user should be running.

"""
from time import sleep
import sys
import Globals
import Config
from KeyDetectors import StartKeyDetection
import AudioPlayer
import FileExplorer
import DisplayController
from Dictionaries import OS_DICT
import yappi


yappi.start
def main():
    '''
    Initialized and runs all the various threads, then sleeps until a KeyboardInturrupt occurs.
    '''
    Config.init()
    Globals.init()
    Globals.OS_DETECTED = DetectOS()
    AudioPlayer.init()
    AudioPlayer.StartAudioController()
    FileExplorer.init()
    FileExplorer.StartFileController()
    DisplayController.StartDisplayController()
    Globals.ReadyChecks.Main = True

    # Begin starting up threads
    StartKeyDetection()
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
    Globals.Quit = True
    while Globals.ReadyChecks.KeyDetector is True or Globals.ReadyChecks.Display is True or Globals.ReadyChecks.Audio is True or Globals.ReadyChecks.FileController is True:
        sleep(0.5)
    print("All threads have quit, quitting!")
