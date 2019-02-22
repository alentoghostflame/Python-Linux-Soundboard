from os import listdir
import threading
from time import sleep, time
from Globals import global_variables
import Config
from Logger import *



def init():
    pass


def StartFileController():
    FileController = threading.Thread(target=FileLogic)
    FileController.start()
    global_variables.online.file_controller = True


def FileLogic():
    '''
    This is the logic for the file explorer. It handles the + and - keys for changing pages (also known as folders) as
    well as reading all the files. It reads the file paths as well as the file names, and puts them in
    Globals.FileTracker.
    '''
    while True:
        StartLogic = time()  # Start Time for the File Polling Limit set in the config.

        ''' Index the Folders holding the sound files. '''
        IndexSoundFolders(Config.Config.RootSoundFolder)
        global_variables.file.folder_index = IndexItemName(Config.Config.RootSoundFolder)

        ''' Detection for the + and - keys. '''
        if global_variables.input.write_ready is False:
            if global_variables.input.key is 11:
                global_variables.input.page += 1
                if global_variables.input.page > global_variables.file.total_folders:
                    global_variables.input.page = 1
                global_variables.input.write_ready = True
            elif global_variables.input.key is 10:
                global_variables.input.page -= 1
                if global_variables.input.page < 1:
                    global_variables.input.page = global_variables.file.total_folders
                global_variables.input.write_ready = True

        ''' Index both the names and the paths of the audio files. '''
        IndexSoundFiles(global_variables.file.folder_path_index[(global_variables.input.page - 1)])
        global_variables.file.file_index = IndexItemName(global_variables.file.folder_path_index[(global_variables.input.page - 1)])

        if global_variables.misc.quit == True:
            print("File Controller Thread is OUT!")
            global_variables.online.file_controller = False
            return
        ''' Tick limiter, to prevent the thread from running as fast as it can. '''
        EndLogic = time()
        TimeDiff = EndLogic - StartLogic
        if TimeDiff < Config.Config.FilePollingRate:
            sleep(Config.Config.FilePollingRate - TimeDiff)


def IndexFolder(FolderPath):
    ''' This function indexes the inside of a single folder. Returns a list of items (files or folders) inside the
    folder that is searched. FolderPath is the path to the folder it searches inside of. Note, only grabs the NAME
    of the items, and not the path.
    :param FolderPath: Path to the folder to search inside of.
    :return: A list of all the names of the items found.
    '''
    FolderItems = listdir(FolderPath)
    Counter = 1
    DoneYet = False
    IndexFolder = []

    while not DoneYet:
        DoneYet = True
        for Item in FolderItems:
            try:
                if eval(Item[0]) == Counter:
                    Counter += 1
                    DoneYet = False
                    IndexFolder.append(Item)
            except NameError:
                pass
    return IndexFolder


def IndexItemName(FolderPath):
    '''
    Similar to IndexFolder(), but removes the number and whitespace prefix of the items found.
    :param FolderPath: Path to the folder to search inside of.
    :return: A list of all the names of the items found, with the first 2 characters removed.
    '''
    FolderItems = listdir(FolderPath)
    Counter = 1
    DoneYet = False
    IndexFolder = []

    while not DoneYet:
        DoneYet = True
        for Item in FolderItems:
            temp = 0
            try:
                if eval(Item[0]) == Counter:
                    Counter += 1
                    DoneYet = False
                    IndexFolder.append(Item[2:])
            except NameError:
                pass
    return IndexFolder


def IndexSoundFolders(FolderPath):
    '''
    Indexes the inside of the folder, and sets Globals.FileTracker.FolderPathIndex to the file path location of all
    found folders relative to the script, and increases Globals.FileTracker.TotalFolders by 1 for each folder found.
    :param FolderPath: Path to the folder to search inside of.
    '''
    Folders = IndexFolder(FolderPath)
    global_variables.file.folder_path_index = []
    global_variables.file.total_folders = 0
    for Folder in Folders:
        global_variables.file.folder_path_index.append(FolderPath + "/" + Folder)
        global_variables.file.total_folders += 1


def IndexSoundFiles(FolderPath):
    '''
    Indexes the inside of the folder, and sets Globals.FileTracker.FolderPathIndex to the file path location of all
    found sound files relative to the script. Built for Linux, NOT for Windows.
    :param FolderPath: Path to the folder to search inside of
    '''
    Files = IndexFolder(FolderPath)
    global_variables.file.file_path_index = []
    for File in Files:
        temp = FolderPath + "/" + File
        temp = temp.replace(" ", "\\ ")
        global_variables.file.file_path_index.append(temp)

