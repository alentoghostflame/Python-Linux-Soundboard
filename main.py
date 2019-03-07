#!/usr/bin/env python3
"""

The main start file for Python Voice Chat Soundboard.
Main.py starts up the program and tells the various parts of it to shutdown when needed. The user should run this file.

"""
from time import sleep
from globals import global_variables, global_config
from logger import log, INFO, WARNING, ERROR
import input_controller
import audio_controller
import display_controller


def main():
    """
    Go into a display loop until the display is canceled for whatever reason.
    TKinter demands to have the window be run in the main thread, unfortunately.
    """
    global_variables.online.main = True
    if global_config.main.use_gui is False:
        display_controller.display_terminal_output()
    else:
        display_controller.run_gui()


try:
    """
    Have the file_controller initially read everything, the audio_controller startup the null-sink and loopback, the 
    input_controller get inputs (if needed), and finally get the main thread in the display loop.
    Once the window is closed, main will tell all the threads to stop 
    """
    log(INFO, "main", "Beginning program execution.")
    # global_variables.misc.os_detected = detect_os()
    audio_controller.start_audio_setup()
    input_controller.start_input_controller()
    main()
    global_variables.misc.quit = True
    audio_controller.end_audio_setup()
    while global_variables.online.key_detector is True or global_variables.online.input_controller is True:
        sleep(0.5)
    log(INFO, "main", "All threads have quit in some manner, quitting!")

except KeyboardInterrupt:
    # If a keyboard interrupt is done for some reason, kill threads, null-sink, and loopback.
    global_variables.misc.quit = True
    audio_controller.end_audio_setup()
    while global_variables.online.key_detector is True or global_variables.online.input_controller is True:
        sleep(0.5)
    log(INFO, "main", "All threads have quit in some manner, quitting!")
