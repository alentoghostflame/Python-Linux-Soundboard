import struct
import threading
import subprocess as sp
from DisplayController import play_buttons
from time import sleep
from Globals import global_variables, global_config
from AudioController import audio_logic
from Logger import log, INFO, WARNING, ERROR
from Dictionaries import KEY_CODES


def start_input_controller():
    """
    If there is something in the event_file_location, start up key_detection in a seperate thread.
    Else, don't do anything.
    :return: None
    """
    if global_variables.input.event_file_location is not None and global_variables.input.key_detection_started is False:
        log(INFO, "start_input_controller", "Starting Linux key detection.")
        key_detector = threading.Thread(target=key_detection)
        key_detector.start()
    elif global_variables.input.key_detection_started is True:
        log(WARNING, "start_input_controller", "Key detection already started, not starting key detection.")
    else:
        log(INFO, "start_input_controller", "event_file_location set to None, not starting key detection.")


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


def key_detection():
    """
    Attempts to open the event file given by event_file_location. If there is a permission error, execute
    chown_event_file and try one more time. If the file isn't found, raise a not implemented error.
    Read the file, and unpack the information its giving. Use most of that information to determine if the user is
    pressing a key relevant to this program. (relevancy is determined using KEY_CODES in dictionaries)
    If the pressed key is relevant, forward that key to input_logic.
    If the pressed key is not relevant, ignore it.
    If the quit variable is True, shut down the thread.
    NOTE: The information on how to unpack things was taken from StackOverflow. If there are any suggestions on how to
    make this more efficient/better to read, that would be great.
    :return: None
    """
    try:
        keyboard_input = open(global_variables.input.event_file_location, "rb")
    except PermissionError:
        chown_event_file(global_variables.event_file_location)
        keyboard_input = open(global_variables.input.event_file_location, "rb")
    except FileNotFoundError:
        raise NotImplementedError

    global_variables.input.key_detection_started = True

    # These next 5 lines were taken from StackOverflow (kind of, made some modifications).
    jank_format = 'llHHI'
    event_size = struct.calcsize(jank_format)
    event = keyboard_input.read(event_size)
    while event:
        (tv_sec, tv_usec, key_type, code, value) = struct.unpack(jank_format, event)

        if (key_type != 0 or code != 0) and code != 4 and value == 1:
            # print("Event type %u, code %u, value %u at %d.%d" % (key_type, code, value, tv_sec, tv_usec))
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
            global_variables.input.key_detection_started = False
            global_variables.online.key_detector = False
            return 0


def event_file_checker(input_path):
    """
    Quickly detect if a file can be opened and closed by the program.
    :param input_path: Path to the file to be checked.
    :return: 0 for success.
    """
    event_file = open(input_path, "rb")
    event_file.close()
    return 0


def input_logic(input_key):
    """
    Perform an action for a given input_key. If one through nine, attempt to play the audio file associated with that
    number. If zero, attempt to kill all audio processes. If ten (minus key) execute back_page. if eleven (plus key)
    execute forward_page.
    If any number is given other than the ones above, raise a not implemented error, because nothing else is
    implemented.
    :param input_key: Input key, already processed through Dictionaries.KEY_CODES.
    :return: None
    """
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
        log(ERROR, "input_logic", "Input key \"" + input_key + "\" was pressed, there is no handler for that key!")
        raise NotImplementedError
