# Python-Linux-Soundboard
I couldn't find any soundboards compatable with Linux that fit my standards, so I made my own that uses the numpad.

![alt text](https://i.imgur.com/VJvxTBk.png "Screenshot")

## Requirments
`Pulseaudio`, `TKinter`, and Python 3. The commands used in this are `pactl` and `paplay` to create an audio device and to stream audio to the audio device, and `Tkinter` is used to make the GUI. All this was written in Python 3. A soft requirement is `pavucontrol` to set an application to listen to the monitor of PythonSoundboardOutput (AKA PythonSoundboardOutput.monitor)

## Quick Feature List
* Supports multiple folders, and allows quickly changing between those folders.
* Control the sounds played and folder selected via numpad keys.
* Kill all outgoing audio via 0/Zero.

## How to get TKinter
If on Ubuntu, do `sudo apt install python3-tk` to get TKinter for Python3. Else, use pip to install it.

### Initial Setup
First thing you need to do is edit the `EventFileLocation` inside `Config.py`. You can find the `EventFileLocation` of your keyboard by using the `cat` command on various event files inside `/dev/input/`. Example, `sudo cat /dev/input/event3`. If you find one that spits out text every time you press a key, chances are that's the event file. Everything else can be left alone by default.

### Adding Audio Files/Folders
#### Folders
Inside of the `RootSoundFolder` (Default: Sound Files, configurable in `Config.py`), there is already a folder named `1 Example`.

To add additional folders to be read by the soundboard, you make a folder that starts with a number, then you put the name with a space between the number and the name.

Example, `5 Taunt Sounds`.
Another example,`1 Foo`, `2 Bar`, `3 Yadda`, `4 Yeeda`.

There is no limit to the maximum number of folders (theoretically).

 A properly placed folder will have a file structure similar to `RootSoundFolder/1 Foo/`, assuming `1 Foo` is the name of the folder you placed.

#### Audio Files
To add audio files, you put them inside of a folder with a similar naming scheme. Note that the number at the beginning of the audio file name wont corrospond with the numpad key to play the audio file if you skip numbers.

There is no limit of audio files in a single folder (theoretically), but the buttons and numpad can only use the first 9.

A properly placed audio file will have a file structure similar to `RootSoundFolder/1 Foo/1 Bar.wav`, assuming `1 Foo` is the name of the folder and `1 Bar.wav` is the name of the audio file.

Note, you can have whatever audio files that `paplay` is able to handle run (theoretically), but only `.wav` and `.ogg` files have been tested so far.

### Running
Run `Main.py` inside a terminal. Using Ubuntu 18.04, run `python3 Main.py` in the directory that `Main.py` is located in. Once you do that, it should be up and running.

### How to Actually Use
1. Use whatever method you know to set an application to listen to the monitor of `PythonSoundboardOutput` (AKA `PythonSoundboardOutput.monitor`).
  If you don't know how to do that and either can or have `pavucontrol` installed, read this.
  1. install `pavucontrol` if you don't have it. If you do, run it.
  2. Once ran, a window with various tabs on top should have popped up. What we are interested in is the Recording tab. Open that, and you should see at least 2 entries. 
     - If the only entry you see is something that starts with `Loopback`, that means that no applications are attempting to record your microphone, but the soundboard is active. To fix that, get the application you want to use the soundboard on to attempt to record your microphone. On Discord for example, that means entering a voice room. Once you do that, an entry should pop up.
     - If NO entires are there, that means the soundboard is either not running or something errored.

  3. Top right of the entry is a small box with something in it, probably the name of the currently plugged in microphone. Click on it, then switch it to `Monitor of Python_Soundboard_Output`.

2. With that done, use the Numpad numbers to play the various audio files you assigned to them, and press the `+` and `-` keys to switch pages (AKA folders).


