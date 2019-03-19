#!/usr/bin/env python3
"""

The main start file for Python Voice Chat Soundboard. The user should run this file.
Main.py starts up the program, runs the frontend, and tells the various parts of it to shutdown when needed.

"""
from time import sleep
from globals import global_variables, global_config
from logger import log, INFO, WARNING, ERROR
import input_controller
import audio_controller
import display_controller


def main():
    """
    Report main as online.
    Depending on the config setting, either run the terminal-based frontend or the TKinter based frontend.
    Both of these frontend choices should be a loop of some kind. The try-catch below currently relies on that.

    Reason for having main control the graphical frontend: TKinter demands that the window be run in the main thread,
    and not a threading thread. To keep consistency and reduce complexity, run both options in the main thread.
    """
    global_variables.online.main = True
    if global_config.main.use_gui is False:
        display_controller.display_terminal_output()
    else:
        display_controller.run_gui()


try:
    """
    Create the PythonSoundboardOutput null-sink and (if specified in the config) Loopback.
    Start up the input_controller thread.
    Run the frontend.
    
    Once the frontend has exited, give the signal for all existing threads to terminate themselves, unload the
    PythonSoundboardOutput null-sink and (if specified in the config) Loopback.
    Then wait until all child threads to report offline before exiting.
    
    If a KeyboardInterrupt were to happen, give the signal for all existing threads to terminate themselves, unload the
    PythonSoundboardOutput null-sink and (if specified in the config) Loopback.
    Then wait until all child threads to report offline before exiting.
    """
    log(INFO, "main", "Beginning program execution.")
    # global_variables.misc.os_detected = detect_os()
    audio_controller.start_audio_setup()
    input_controller.start_input_controller()
    main()
    global_variables.misc.quit = True
    audio_controller.end_audio_setup()
    while global_variables.online.key_detector is True:
        sleep(0.5)
    log(INFO, "main", "All threads have quit in some manner, quitting!")

except KeyboardInterrupt:
    # If a keyboard interrupt is done for some reason, kill the threads, null-sink, and loopback.
    global_variables.misc.quit = True
    audio_controller.end_audio_setup()
    while global_variables.online.key_detector is True:
        sleep(0.5)
    log(INFO, "main", "All threads have quit in some manner, quitting!")
