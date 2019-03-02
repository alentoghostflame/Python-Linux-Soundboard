# Python-Linux-Soundboard
I couldn't find any soundboards compatable with Linux that fit my standards, so I made my own that uses the numpad.

![alt text](https://i.imgur.com/OBjysfk.png "Screenshot")

## Requirments
`Pulseaudio`, `TKinter`, and Python 3. The commands used in this are `pactl` and `paplay` to create an audio device and to stream audio to the audio device, and `Tkinter` is used to make the GUI. All this was written in Python 3. A soft requirement is `pavucontrol` to set an application to listen to the monitor of PythonSoundboardOutput (AKA PythonSoundboardOutput.monitor)

## Quick Feature List
* Supports multiple folders, and allows quickly changing between those folders.
* Control the sounds played and folder selected via numpad keys (If given an event file).
* Multiple audio threads allowing for multiple different or same sounds to play at once!
* Ability to instantly kill all audio threads.

## No module named 'tkinter'!
If on Ubuntu, do `sudo apt install python3-tk` to get TKinter for Python3. Else, use pip to install it or find instructions for your distribution.

## How to...
Small list of "How to do"'s, if you either have a question or found something that you think belongs here, make an issue for it and I'll probably add it!

### ...make numpad controls work?
Find your event file for your keyboard. To do that, open up a terminal and run `sudo cat /dev/input/event#`, replacing `#` with a number (such as `1`), and press some keys on your keyboard. If stuff pops up every time you press a key, that's the event file you are looking for. If not, go to the next number.

Once you have the path to the event file (ex: `/dev/input/event4`), open up the soundboard, enter it into the entry box at the top, and press "Use Event File". Follow the prompts and you should be good to go!

Controls are as follows: Numbers 1 through 9 play the 1st through 9th sounds on the list to the right. + goes down/forward a folder, - goes up/back a folder. Folders are displayed in the list to the left. The number 0 will terminate all currently playing audio from the soundboard.

### ...make applications listen to this?
Not super hard. Using Pulseaudio Volume Control (pavucontrol) you can set the recording application of choice to listen to `PythonSoundboardOutput.monitor`. Doing that will cause the application to only be able to hear the soundboard.

Don't have Pulseaudio Volume Control (pavucontrol)? On Ubuntu, do `sudo apt install pavucontrol` to install it.

Don't want to use Pulseaudio Volume Control? Maybe my other github project will help you, the [Pulseaudio-Loopback-Tool.](https://github.com/alentoghostflame/Python-Pulseaudio-Loopback-Tool) If you use that, create a remapped source with `PythonSoundboardOutput.monitor`, and it should show up as an available mic inside applications.


## Adding Audio Folders/Files
#### Folders
Inside of the `RootSoundFolder` (Default: Sound Files, configurable in `Config.py`), there is already a folder named `1 Example`.

To add additional folders to be read by the soundboard, you make a folder that starts with a number, then you put the name with a space between the number and the name. Example, `5 Taunt Sounds`. Another example,`1 Foo`, `2 Bar`, `3 Yadda`, `4 Yeeda`.

There is no limit to the maximum number of folders (theoretically).

 A properly placed folder will have a file structure similar to `RootSoundFolder/1 Foo/`, assuming `1 Foo` is the name of the folder you placed.

#### Audio Files
To add audio files, you put them inside of a folder with a similar naming scheme. Note that the number at the beginning of the audio file name wont corrospond with the numpad key to play the audio file if you skip numbers.

There is no limit of audio files in a single folder (theoretically), but the buttons and numpad can only use the first 9.

A properly placed audio file will have a file structure similar to `RootSoundFolder/1 Foo/1 Bar.wav`, assuming `1 Foo` is the name of the folder and `1 Bar.wav` is the name of the audio file.

Note, you can have whatever audio files that `paplay` is able to handle run (theoretically), but only `.wav` and `.ogg` files have been tested so far.

### Running
Run `Main.py` inside a terminal. Using Ubuntu 18.04, run `python3 Main.py` in the directory that `Main.py` is located in. Once you do that, it should be up and running.

## "I want ____" or "How do I do ____?"

If you have any questions, concerns, ideas, etc, make an issue for it! I'm all up for recommendations on how to make this better.


