import threading
import subprocess
from time import time, sleep
import Globals
import Config


def StartAudioController():
    AudioController = threading.Thread(target=AudioLogic)
    AudioController.start()
    Globals.ReadyChecks.Audio = True



def AudioLogic():
    StartAudioSetup()
    while True:
        StartLogic = time()

        AudioKeyDetection()

        if Globals.Quit is True:
            EndAudioSetup()
            print("Audio Controller Thread is OUT!")
            Globals.ReadyChecks.Audio = False
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

    if Globals.KeyPressed.WrittenTo is True and Globals.KeyPressed.Key is not 10 and Globals.KeyPressed.Key is not 11:
        if Globals.KeyPressed.Key is 0:
            Globals.KeyPressed.WrittenTo = False
        elif Globals.KeyPressed.Key > 0 and Globals.KeyPressed.Key < 10:
            if len(Globals.FileTracker.FilePathIndex) > Globals.KeyPressed.Key - 1:
                AudioThread = threading.Thread(target=PlayAudioFile, args=(Globals.FileTracker.FilePathIndex[(Globals.KeyPressed.Key - 1)],))
                AudioThread.daemon = True
                AudioThread.start()
            Globals.KeyPressed.WrittenTo = False


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




