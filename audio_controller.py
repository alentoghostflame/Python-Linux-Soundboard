import threading
import subprocess
import DisplayController
from time import sleep
from Globals import global_variables, global_config
from Logger import log, INFO  # , WARNING, ERROR


def fix_audio_path(input_path):
    """
    Fixes the audio path string to be usable by commands outside of Python. While Python automatically handles spaces
    inside of path strings, commands executed using subprocess.call() do not. This essentially replaces all spaces
    with a backslash plus a space. Example: " " -> "\ "
    If any more escapes need to be added to get weirdly named audio files to play, add them here.
    :param input_path: Input path in need of backslashes behind the spaces.
    :return: Fixed path with backslashes behind the spaces.
    """
    output_path = input_path.replace(" ", "\\ ")
    return output_path


def audio_logic(input_folder_index, input_file_index):
    """
    Get the local file_paths from the global file_paths with an input_folder_index value.
    If there are greater than or equal file paths than the input_file_index(asking for a file path that doesn't exist)
    and the current thread count is less than the max threads, get a good_file_path, and make a new thread to play the
    audio file at that path.

    Else, dont do anything.
    :param input_folder_index: An integer corresponding to global_variables.file.folder_names
    :param input_file_index: An integer corresponding to global_variables.file.file_names
    :return: None
    """
    file_paths = global_variables.file.file_paths[input_folder_index]
    if len(file_paths) - 1 >= input_file_index and \
            global_config.audio.max_audio_threads > global_variables.audio.thread_count:
        good_file_path = fix_audio_path(file_paths[input_file_index])
        audio_thread = threading.Thread(target=play_audio_file, args=(good_file_path,))
        audio_thread.start()
    else:
        pass


def play_audio_file(path_to_file):
    """
    Increment the thread_count by one, and update the thread_count on the GUI.
    Launch the command to play the audio file. After that, check if the command is still running. If it is, sleep for
    the polling_rate, else go on. If kill_audio is ever set to True while the command is running, terminate the audio
    process.
    Decrement the thread_count by one, and update the thread_count on the GUI.
    :param path_to_file: The path of the audio file to be played. Should have escapes behind necessary characters.
    :return: 0
    """
    global_variables.audio.thread_count += 1
    DisplayController.frame_top.update_thread_count()
    audio = subprocess.Popen("exec paplay --device=PythonSoundboardOutput " + path_to_file, shell=True,
                             stdout=subprocess.PIPE)

    while audio.poll() is None:
        if global_variables.audio.kill_audio is True:
            audio.terminate()
            break
        else:
            sleep(global_config.audio.polling_rate)

    global_variables.audio.thread_count -= 1
    DisplayController.frame_top.update_thread_count()
    return 0


def start_audio_setup():
    """
    Create the null sink that the soundboard will output to, and export the ID to null_sink
    If the create_loopback config option is True, create a loopback with the source of the null sink previously created,
    and export the ID to loopback.
    :return: None
    """
    audio_start_command = """ pactl load-module module-null-sink sink_name=PythonSoundboardOutput 
    sink_properties=device.description="Python_Soundboard_Output" rate=48000 """
    loopback_start_command = """ pactl load-module module-loopback source=PythonSoundboardOutput.monitor 
    latency_msec=5 """
    log(INFO, "start_audio_setup", "Creating null sink.")
    global_variables.audio.null_sink = eval(subprocess.check_output(audio_start_command, shell=True))
    if global_config.audio.create_loopback is True:
        log(INFO, "start_audio_setup", "Creating loopback.")
        global_variables.audio.loopback = eval(subprocess.check_output(loopback_start_command, shell=True))


def end_audio_setup():
    """
    Kill all running audio processes by setting kill_audio to True, waiting the polling_rate, then setting kill_audio
    back to False.
    If the create_loopback config option is True, unload the loopback with the source as the soundboards null-sink using
    the ID from loopback.
    Unload the null-sink that the soundboard is outputting to using the ID from null-sink.
    :return: None
    """
    log(INFO, "end_audio_setup", "Killing all running audio threads.")
    global_variables.audio.kill_audio = True
    sleep(global_config.audio.polling_rate)
    global_variables.audio.kill_audio = False
    if global_config.audio.create_loopback is True:
        log(INFO, "end_audio_setup", "Removing loopback.")
        subprocess.call("pactl unload-module " + str(global_variables.audio.loopback), shell=True)
    log(INFO, "end_audio_setup", "Removing null sink.")
    subprocess.call("pactl unload-module " + str(global_variables.audio.null_sink), shell=True)






