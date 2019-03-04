#!/usr/bin/env python3
"""

The main start file for Python Voice Chat Soundboard.
Main.py starts up the threads and tells them to shut down when need be. This is the file that a user should be running.

"""
from time import sleep
import sys
from Globals import global_variables, global_config
from Logger import log, INFO  # , WARNING, ERROR
import InputController
import AudioController
import FileController
import DisplayController
from Dictionaries import OS_DICT


def main():
    """
    Go into a display loop until the display is canceled for whatever reason.
    TKinter demands to have the window be run in the main thread, unfortunately.
    """
    global_variables.online.main = True
    if global_config.main.use_gui is False:
        DisplayController.display_terminal_output()
    else:
        DisplayController.run_gui()


def detect_os():
    return OS_DICT[sys.platform]


try:
    """
    Have the file_controller initially read everything, the audio_controller startup the null-sink and loopback, the 
    input_controller get inputs (if needed), and finally get the main thread in the display loop.
    Once the window is closed, main will tell all the threads to stop 
    """
    log(INFO, "main", "Beginning program execution.")
    global_variables.misc.os_detected = detect_os()
    FileController.refresh_files()
    AudioController.start_audio_setup()
    InputController.start_input_controller()
    main()
    global_variables.misc.quit = True
    AudioController.end_audio_setup()
    while global_variables.online.key_detector is True or global_variables.online.input_controller is True:
        sleep(0.5)
    log(INFO, "main", "All threads have quit in some manner, quitting!")

except KeyboardInterrupt:
    global_variables.misc.quit = True
    AudioController.end_audio_setup()
    while global_variables.online.key_detector is True or global_variables.online.input_controller is True:
        sleep(0.5)
    log(INFO, "main", "All threads have quit in some manner, quitting!")
