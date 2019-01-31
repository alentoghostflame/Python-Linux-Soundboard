import threading
import subprocess
from time import time, sleep
import Globals
import Config


def init():
    global AudioStartCommandText
    global AudioStartCommandArray
    global LoopbackStartCommandArray
    global AudioEndCommandText
    global AudioEndCommandArray
    global LoopbackEndCommandArray

    AudioStartCommandText = """ pactl load-module module-null-sink sink_name=PythonAudioboardOutput sink_properties=device.description="Python_Audioboard_Output" rate=48000 """
    AudioStartCommandArray = ["pactl", "load-module", "module-null-sink", "sink_name=PythonAudioboardOutput", """ sink_properties=device.description="Python_Audioboard_Output" """, "rate=48000"]
    LoopbackStartCommandArray = ["pactl", "load-module", "module-loopback", "source=PythonAudioboardOutput.monitor"]
    AudioEndCommandText = """ pactl unload-module module-null-sink """
    AudioEndCommandArray = ["pactl", "unload-module", "module-null-sink"]
    LoopbackEndCommandArray = ["pactl", "unload-module", "module-loopback"]


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
    subprocess.call("paplay --device=PythonAudioboardOutput " + pathtofile, shell=True)
    return 0


def StartAudioSetup():
    subprocess.call(AudioStartCommandText, shell=True)
    subprocess.call(LoopbackStartCommandArray)


def EndAudioSetup():
    subprocess.call(AudioEndCommandArray)
    subprocess.call(LoopbackEndCommandArray)




