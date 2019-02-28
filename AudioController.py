import threading
import subprocess
from time import time, sleep
from Globals import global_variables
from Config import global_config
from Logger import log, INFO, WARNING, ERROR


# Variables meant specifically for the Audio Controller
audio_thread_count = 0


def start_audio_controller():
    audio_controller = threading.Thread(target=audio_loop)
    audio_controller.start()
    global_variables.online.audio_controller = True


def audio_loop():
    start_audio_setup()
    while True:
        start_of_logic = time()

        audio_logic()

        if global_variables.misc.quit is True:
            end_audio_setup()
            log(INFO, "AudioLogic", "Shutting down!")
            global_variables.online.audio_controller = False
            return

        ''' Tick limiter, to prevent the thread from running as fast as it can. '''
        end_of_logic = time()
        time_difference = end_of_logic - start_of_logic
        if time_difference < global_config.audio.polling_rate:
            sleep(global_config.audio.polling_rate - time_difference)


def audio_logic():
    '''
    Queries the last pressed viable key and checks if the key is the numpad 0 through 9 keys via Globals.KeyPressed.Key.
    If it is one of those keys, it performs an action and allows KeyDetectors to write a new key. Keys 1-9 will play
    the sound file associated with that number in Globals.FileTracker.FilePathIndex. Key 0 currently does nothing.
    :return: No return value.
    '''
    # If the key has been written to, AND if the key is between 0 and 9...
    if global_variables.input.write_ready is False and global_variables.input.key < 10:
        # If the key corresponds to 0, simply set write_ready to True to allow new values to be read.
        if global_variables.input.key is 0:
            # This is an empty function, something new can be put here.
            global_variables.input.write_ready = True

        # If the key is greater than 0 but less than 10, the max sound thread count hasn't been reached, and the File
        # Controller reports a path for the audio file corresponding to the key pressed, play the sound in another
        # thread.
        elif global_variables.input.key > 0:
            # Make sure the File Controller set a path for the audio file corresponding to the key pressed.
            if len(global_variables.file.file_path_index) > global_variables.input.key - 1:
                # Make sure there are not more audio threads going than the max sound threads specified in Config.
                if global_config.audio.max_sound_threads > audio_thread_count:
                    audio_thread = threading.Thread(target=play_audio_file, args=(global_variables.file.file_path_index
                                                                                  [(global_variables.input.key - 1)],))
                    audio_thread.daemon = True
                    audio_thread.start()
                else:
                    pass
                pass
            # No matter if an audio file was played or not, let Key Detector know to put in a new key.
            global_variables.input.write_ready = True


def play_audio_file(pathtofile):
    global audio_thread_count
    audio_thread_count += 1
    subprocess.call("paplay --device=PythonSoundboardOutput " + pathtofile, shell=True)
    audio_thread_count -= 1
    return 0


def start_audio_setup():
    audio_start_command = """ pactl load-module module-null-sink sink_name=PythonSoundboardOutput 
    sink_properties=device.description="Python_Soundboard_Output" rate=48000 """
    loopback_start_command = """ pactl load-module module-loopback source=PythonSoundboardOutput.monitor 
    latency_msec=5 """
    subprocess.call(audio_start_command, shell=True)
    if global_config.audio.create_loopback is True:
        subprocess.call(loopback_start_command, shell=True)


def end_audio_setup():
    audio_end_command = """ pactl unload-module module-null-sink """
    subprocess.call(audio_end_command, shell=True)
    loopback_end_command = """ pactl unload-module module-loopback """
    subprocess.call(loopback_end_command, shell=True)




