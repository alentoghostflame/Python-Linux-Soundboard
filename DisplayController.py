import sys
import threading
from time import sleep, time
import Globals
import Config


def MoveCursorUp(Height):
    for i in range(Height):
        sys.stdout.write("\033[F")


def StartDisplayController():
    DisplayController = threading.Thread(target=DisplayLogic)
    DisplayController.start()
    Globals.ReadyChecks.Display = True


def DisplayLogic():
    sleep(1)
    while True:
        StartLogic = time()

        DisplayFrame()

        if Globals.Quit == True:
            print("Display Controller Thread is OUT!")
            Globals.ReadyChecks.Display = False
            return
        ''' Tick limiter, to prevent the thread from running as fast as it can. '''
        EndLogic = time()
        TimeDiff = EndLogic - StartLogic
        if TimeDiff < Config.Config.DisplayPollingRate:
            sleep(Config.Config.DisplayPollingRate - TimeDiff)


def DisplayFrame():
    SongList = []
    temp = 0
    RealSongLength = len(Globals.FileTracker.FileIndex)
    while temp < 9:
        if temp < RealSongLength:
            SongList.append(Globals.FileTracker.FileIndex[temp])
        else:
            SongList.append("Empty")
        temp += 1

    print("■════════════════════════════════════■")

    CurrentPage = Globals.KeyPressed.Page
    MaxPages = Globals.FileTracker.TotalFolders
    temp = "- Page " + str(CurrentPage) + " of " + str(MaxPages) + " +"
    temp = '{:26}'.format(temp)
    print("║          ", temp, end="")
    print("║")
    temp = '{:24}'.format(Globals.FileTracker.FolderIndex[CurrentPage - 1][:23])
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


