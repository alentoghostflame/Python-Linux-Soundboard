import struct
import threading
import subprocess as sp
from DisplayController import play_buttons
from time import sleep
from Globals import global_variables, global_config
from AudioController import audio_logic
from Logger import log, INFO  # , WARNING, ERROR
from Dictionaries import KEY_CODES


def start_input_controller():
    """
    Get the OS type. If Linux, start up key_detection_linux() in another thread. If any other OS type, raise a
    NotImplementedError because other types are not implemented.
    :return: None
    """
    if global_config.audio.event_file_location is not None:
        log(INFO, "start_input_controller", "Starting Linux key detection.")
        key_detector = threading.Thread(target=key_detection_linux)
        key_detector.start()
    else:
        log(INFO, "start_input_controller", "event_file_location set to None, not starting.")


def chown_event_file(event_file_path):
    """
    Takes in the path to an event file that needs to be chown'd, and launches a gnome-terminal with the chown command
    running in it, and awaiting the sudo password of the user if the file exists.
    :param event_file_path: String containing the file path to the event file to be chown'd.
    :return: None
    """
    log(INFO, "chown_event_file", "Executing chown on \"" + event_file_path + "\".")
    command = sp.Popen("gnome-terminal --window --title=\"Fix Permission of " + event_file_path +
                           "\" --wait -- sudo chown $USER:$USER " + event_file_path, stdout=sp.PIPE, shell=True)
    while command.poll() is None:
        sleep(0.5)


def key_detection_linux():
    """
    Attempts to open the event file given by global_config.event_file_location. If there is a PermissionError, execute
    chown_event_file(global_config.event_file_location) and attempt to reopen it. If there is a FileNotFoundError,
    raise a NotImplementedError. Then, disable the event_blocker to allow main to continue running more threads.
    Things get a bit hairy from here.
    Regarding the input, I dont fully understand how everything works. I found the format that the event file outputs
    every time a key is pressed on StackOverflow, along with a bunch of code. I took that code, and somewhat modified it
    for my purposes. Essentially, every time a key is pressed the event file will spit out data. Take that data, unpack
    it into information, and use that information with the program.
    If it looks like a key got pressed down and global_variables.input.write_ready is True, run the key through the
    KEY_CODES dictionary. If it's in there set global_variables.input.key equal to it and set
    global_variables.input.write_ready to False.
    :return: None
    """
    try:
        keyboard_input = open(global_config.audio.event_file_location, "rb")
    except PermissionError:
        chown_event_file(global_config.event_file_location)
        keyboard_input = open(global_config.audio.event_file_location, "rb")
    except FileNotFoundError:
        raise NotImplementedError

    global_variables.misc.key_detection_started = True

    # These next 5 lines were taken from StackOverflow (kind of, made some modifications).
    jank_format = 'llHHI'
    event_size = struct.calcsize(jank_format)
    event = keyboard_input.read(event_size)
    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(jank_format, event)

        if (type != 0 or code != 0) and code != 4 and value == 1:
            # print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
            output_key = KEY_CODES.get(code, 666)
            if output_key != 666:
                input_logic(output_key)
            else:
                pass
        else:
            pass
        event = keyboard_input.read(event_size)

        if global_variables.misc.quit is True:
            log(INFO, "key_detection_linux", "Shutting down!")
            keyboard_input.close()
            global_variables.online.key_detector = False
            return 0


def event_file_checker(input_path):
    event_file = open(input_path, "rb")
    event_file.close()
    return 0


def input_logic(input_key):
    """

    :param input_key: Input key, already processed through Dictionaries.KEY_CODES.
    :return: None
    """
    ''' If the key is something on the numpad, go through all of this logic. '''
    if 1 <= input_key <= 9:
        audio_logic(global_variables.input.page, input_key - 1)
    elif input_key is 0:
        global_variables.audio.kill_audio = True
        sleep(global_config.audio.polling_rate)
        global_variables.audio.kill_audio = False
    elif input_key is 10:
        play_buttons.back_page()
    elif input_key is 11:
        play_buttons.forward_page()
    else:
        raise NotImplementedError

    pass
