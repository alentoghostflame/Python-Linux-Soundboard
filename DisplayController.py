import sys
import threading
from time import sleep, time
from Globals import global_variables
from Config import global_config
from Logger import *


def MoveCursorUp(Height):
    for i in range(Height):
        sys.stdout.write("\033[F")


def StartDisplayController():
    DisplayController = threading.Thread(target=DisplayLogic)
    DisplayController.start()
    global_variables.online.display_controller = True


def DisplayLogic():
    sleep(1)
    while True:
        StartLogic = time()

        DisplayFrame()

        if global_variables.misc.quit == True:
            print("Display Controller Thread is OUT!")
            global_variables.online.display_controller = False
            return
        ''' Tick limiter, to prevent the thread from running as fast as it can. '''
        EndLogic = time()
        TimeDiff = EndLogic - StartLogic
        if TimeDiff < global_config.display_polling_rate:
            sleep(global_config.display_polling_rate - TimeDiff)


def DisplayFrame():
    if global_config.use_gui is True:
        DisplayFrameGui()
    else:
        DisplayFrameTerminal()


def DisplayFrameGui():
    pass


def DisplayFrameTerminal():
    SongList = []
    temp = 0
    RealSongLength = len(global_variables.file.file_index)
    while temp < 9:
        if temp < RealSongLength:
            SongList.append(global_variables.file.file_index[temp])
        else:
            SongList.append("Empty")
        temp += 1

    print("■════════════════════════════════════■")

    CurrentPage = global_variables.input.page
    MaxPages = global_variables.file.total_folders
    temp = "- Page " + str(CurrentPage) + " of " + str(MaxPages) + " +"
    temp = '{:26}'.format(temp)
    print("║          ", temp, end="")
    print("║")
    temp = '{:24}'.format(global_variables.file.folder_index[CurrentPage - 1][:23])
    print("║            ", temp + "║")
    print("║                                     ║")
    temp1 = '{:8}'.format(SongList[6][:8])
    temp2 = '{:8}'.format(SongList[7][:8])
    temp3 = '{:8}'.format(SongList[8][:8])
    print("║ 7: " + temp1 + " 8: " + temp2 + " 9: " + temp3 + " ║")
    print("║                                     ║")
    temp1 = '{:8}'.format(SongList[3][:8])
    temp2 = '{:8}'.format(SongList[4][:8])
    temp3 = '{:8}'.format(SongList[5][:8])
    print("║ 4: " + temp1 + " 5: " + temp2 + " 6: " + temp3 + " ║")
    print("║                                     ║")
    temp1 = '{:8}'.format(SongList[0][:8])
    temp2 = '{:8}'.format(SongList[1][:8])
    temp3 = '{:8}'.format(SongList[2][:8])
    print("║ 1: " + temp1 + " 2: " + temp2 + " 3: " + temp3 + " ║")
    print("║                                     ║")
    print("■════════════════════════════════════■")
    MoveCursorUp(11)







'''
WxH
39x11
Ideal Layout:
■ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ■
║          - Page 1 of 9 +            ║
║             Classics                ║
║                                     ║
║ 7: SongHere 8: SongHere 9: SongHere ║
║                                     ║
║ 4: SongHere 5: SongHere 6: SongHere ║
║                                     ║
║ 1: SongHere 2: SongHere 3: SongHere ║
║                                     ║
■ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ■
'''


