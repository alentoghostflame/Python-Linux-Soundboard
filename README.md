# Python-Soundboard
CURRENTLY LINUX ONLY.
I couldn't find any soundboards compatable with Linux that fit my standards, so I made my own that uses the numpad.

## Requirments
`Pulseaudio`. The commands used in this are `pactl` and `paplay` to create an audio device and to stream audio to the audio device. A soft requirement is `pavucontrol` to set an application to listen to the monitor of PythonSoundboardOutput (AKA PythonSoundboardOutput.monitor)

## How to Use
Placeholder.

### Initial Setup
First thing you need to do is edit the `EventFileLocation` inside `Config.py`. You can find the `EventFileLocation` of your keyboard by using the `cat` command on various event files inside `/dev/input/`. If you find one that spits out text every time you press a key, chances are that's the event file. Everything else can be left alone by default.

### Adding Audio Files/Folders
#### Folders
Inside of the `RootSoundFolder` (Default: Sound Files, configurable in `Config.py`), there is already a folder named `1 Example`.

To add additional folders to be read by the soundboard, you make a folder that starts with a number, then you put the name with a space between the number and the name.

Example, `5 Taunt Sounds`.

There is currently a limit of 9 different folders. You must name them sequentially (starting at 1), or the soundboard will not find them.

Example, with the folders `1 Foo`, `2 Bar`, `4 Yadda`, `5 Yeeda`, only `1 Foo` and `2 Bar` are going to be read. Note that the numbers indicate what order the folders will be in inside the soundboard.

 A properly placed folder will have a file structure similar to `RootSoundFolder/1 Foo/`, assuming `1 Foo` is the name of the folder you placed.

#### Audio Files
To add audio files, you put them inside of a folder with a similar naming scheme. You have to start 1, and work your way up. Note that the number at the beginning of the audio file name will corrospond with the numpad key to play the audio file.

There is a limit of 9 different audio files that can be assigned inside a single folder.

Just like with the folders, you must name the audio files sequentially (starting at 1), or the soundboard will not find them.

Example, with the audio files `1 Foo.wav`, `2 Bar.wav`, `4 Yadda.wav`, `5 Yeeda.wav`, only `1 Foo.wav` and `2 Bar.wav` are going to be read.

A properly placed audio file will have a file structure similar to `RootSoundFolder/1 Foo/1 Bar.wav`, assuming `1 Foo` is the name of the folder and `1 Bar.wav` is the name of the audio file.

Note, you can have whatever audio files that `paplay` is able to handle run (theoretically), but only Wave files have been tested so far.

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


