import struct
import os
import threading
from Globals import global_variables
import Config
from Logger import *
from Dictionaries import KEY_CODES




def StartKeyDetection():
    temp = global_variables.misc.os_detected
    if temp == 1 or temp == 0:
        print("OS NOT FOUND")
    elif temp == 2:  # If Linux is found...
        print("Linux Found!")
        keydetector = threading.Thread(target=LinuxKeyDetection)
        keydetector.start()
    elif temp == 3:  # If Windows is found...
        print("Windoze Found!")
    elif temp == 4:  # If Mac OS X is found...
        print("JunkOSX Found!")


def LinuxKeyDetection():
    '''
    Opens an event file (Location of that event file is given in Config.Config.EventFileLocation), reads it, and unpacks
    the info in it. 2/5ths of the info unpacked is ignored, as we only need the type, code, and value. If those 3
    variables meet the standards shown below, code is a value listed in Dictionaries.KEY_CODES, and Globals.KeyPressed
    has already been read, then Globals.KeyPressed.Key has the corresponding key written to it and
    Globals.KeyPressed.WrittenTo is set to True. Note, I (Alex Schoenhofen) didn't write all of this myself, and took
    quite a bit here from StackOverflow.
    :return: Nothing notable.
    '''
    try:
        keyboardInput = open(Config.Config.EventFileLocation, "rb")
    except PermissionError:
        ChownEventFile()
        keyboardInput = open(Config.Config.EventFileLocation, "rb")
    except FileNotFoundError:
        # TODO: Make Error Handling for non-existent Event#
        pass
    global_variables.misc.event_blocker = False

    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    event = keyboardInput.read(EVENT_SIZE)
    global_variables.online.key_detector = True

    while event:

        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        if (type != 0 or code != 0) and code != 4 and value == 1:
            # print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
            if global_variables.input.write_ready == True:
                global_variables.input.write_ready = False
                global_variables.input.key = KEY_CODES.get(code, 666)
                if global_variables.input.key == 666:
                    global_variables.input.write_ready = True
        else:
            pass

        event = keyboardInput.read(EVENT_SIZE)
        if global_variables.misc.quit == True:
            print("Key Detection Thread is OUT!")
            keyboardInput.close()
            global_variables.online.key_detector = False
            return 0



def ChownEventFile():
    os.system("sudo chown $USER:$USER " + Config.Config.EventFileLocation)
