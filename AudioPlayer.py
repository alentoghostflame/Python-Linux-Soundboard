import threading
import subprocess
from time import time, sleep
import Globals
from Globals import global_variables
import Config
from Logger import *



def StartAudioController():
    AudioController = threading.Thread(target=AudioLogic)
    AudioController.start()
    global_variables.online.audio_controller = True


def AudioLogic():
    StartAudioSetup()
    while True:
        StartLogic = time()

        AudioKeyDetection()

        if global_variables.misc.quit is True:
            EndAudioSetup()
            print("Audio Controller Thread is OUT!")
            global_variables.online.audio_controller = False
            return
        ''' Tick limiter, to prevent the thread from running as fast as it can. '''
        EndLogic = time()
        TimeDiff = EndLogic - StartLogic
        if TimeDiff < Config.Config.AudioPollingRate:
            sleep(Config.Config.AudioPollingRate - TimeDiff)


def AudioKeyDetection():
    '''
    Queries the last pressed viable key and checks if the key is the numpad 0 through 9 keys via Globals.KeyPressed.Key.
    If it is one of those keys, it performs an action and allows KeyDetectors to write a new key. Keys 1-9 will play
    the sound file associated with that number in Globals.FileTracker.FilePathIndex. Key 0 currently does nothing.
    :return:
    '''

    if global_variables.input.write_ready is False and global_variables.input.key is not 10 and global_variables.input.key is not 11:
        if global_variables.input.key is 0:
            global_variables.input.write_ready = True
        elif global_variables.input.key > 0 and global_variables.input.key < 10:
            if len(global_variables.file.file_path_index) > global_variables.input.key - 1:
                AudioThread = threading.Thread(target=PlayAudioFile, args=(global_variables.file.file_path_index[(global_variables.input.key - 1)],))
                AudioThread.daemon = True
                AudioThread.start()
            global_variables.input.write_ready = True


def PlayAudioFile(pathtofile):
    subprocess.call("paplay --device=PythonSoundboardOutput " + pathtofile, shell=True)
    return 0


def StartAudioSetup():
    AudioStartCommand = """ pactl load-module module-null-sink sink_name=PythonSoundboardOutput sink_properties=device.description="Python_Soundboard_Output" rate=48000 """
    subprocess.call(AudioStartCommand, shell=True)
    LoopbackStartCommand = """ pactl load-module module-loopback source=PythonSoundboardOutput.monitor latency_msec=5 """
    subprocess.call(LoopbackStartCommand, shell=True)
    ''' If you have additional audio setup commands you want to run, place them between here and the end marker. '''

    ''' End Marker '''


def EndAudioSetup():
    AudioEndCommand = """ pactl unload-module module-null-sink """
    subprocess.call(AudioEndCommand, shell=True)
    LoopbackEndCommand = """ pactl unload-module module-loopback """
    subprocess.call(LoopbackEndCommand, shell=True)




