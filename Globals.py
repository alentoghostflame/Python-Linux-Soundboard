'''

The file that contains all the storage locations that will be used in between threads.

'''

def init():
    ''' Initializes all the globals for inter-thread communication. Main.py should be calling this. '''
    global KeyPressed
    global Quit
    global ReadyChecks
    global FileTracker
    global OS_DETECTED
    global EventBlocker
    KeyPressed = KeyPressedClass
    Quit = False
    ReadyChecks = ReadyChecksClass
    FileTracker = FileTrackerClass
    OS_DETECTED = 0
    EventBlocker = True


class KeyPressedClass:
    '''
    Keeps track of what key (if applicable) the user last issued. The Key integer is set to an integer and WrittenTo is
    set to True when KeyDetectors.py detects that the user pressed a key. If WrittenTo is set to True, KeyDetectors.py
    will not write an integer to Key. To have KeyDetectors.py set Key
    '''
    Key = 666
    Page = 1
    WrittenTo = False


class ReadyChecksClass:
    '''
    Keeps track of what threads are running and which ones are not.
    '''
    KeyDetector = False
    Main = False
    Audio = False
    Display = False
    FileController = False


class FileTrackerClass:
    '''
    Keeps a list of Folder names, File names, Folder paths, File paths, and the number of found folders.
    '''
    FolderIndex = []
    FolderPathIndex = []
    TotalFolders = 0
    FileIndex = []
    FilePathIndex = []




