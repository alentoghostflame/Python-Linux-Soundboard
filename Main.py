#!/usr/bin/env python3
"""

The main start file for Python Voice Chat Soundboard.
Main.py starts up the threads and tells them to shut down when need be. This is the file that a user should be running.

"""
from time import sleep
import sys
from Globals import global_variables
from Config import global_config
from Logger import log, INFO  # , WARNING, ERROR
import InputController
import AudioController
import FileController
import DisplayController
from Dictionaries import OS_DICT


def main():
    '''
    Initialized and runs all the various threads, then sleeps until a KeyboardInterrupt occurs.
    '''
    global_variables.misc.os_detected = detect_os()

    ''' If Windows is detected, enable ANSI escape stuff '''
    '''if global_variables.misc.os_detected is 3:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)'''

    InputController.start_input_controller()
    while global_variables.misc.event_blocker is True:
        sleep(0.5)

    if global_config.use_gui is False:
        DisplayController.display_terminal_output()
    else:
        DisplayController.run_gui()

    global_variables.online.main = True

    while True:
        sleep(1)


def detect_os():
    return OS_DICT[sys.platform]


try:
    '''
    The purpose of this try-except is to catch Keyboard Inturrupts and properly close down the threads.
    '''
    log(INFO, "main", "Beginning program execution.")
    FileController.refresh_files()
    AudioController.start_audio_setup()
    main()
except KeyboardInterrupt:
    global_variables.misc.quit = True
    while global_variables.online.key_detector is True or global_variables.online.display_controller is True or \
            global_variables.online.audio_controller is True or global_variables.online.file_controller is True or \
            global_variables.online.input_controller is True:
        sleep(0.5)

    AudioController.end_audio_setup()
    log(INFO, "main", "All threads have quit in some manner, quitting!")
