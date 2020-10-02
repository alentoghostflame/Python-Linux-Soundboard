# Python-Linux-Soundboard
I couldn't find any soundboards compatable with Linux that fit my standards, so I made my own that uses the numpad.

![alt text](https://i.imgur.com/OBjysfk.png "Screenshot")

## Requirments
`Pulseaudio`, `TKinter`, and Python 3. The commands used in this are `pactl` and `paplay` to create an audio device and to stream audio to the audio device, and `Tkinter` is used to make the GUI. All this was written in Python 3. A soft requirement is `pavucontrol` to set an application to listen to the monitor of PythonSoundboardOutput (AKA PythonSoundboardOutput.monitor)


`sudo nano /etc/openal/alsoft.conf` change `#allow-moves=false` to `allow-moves=true`
## Quick Feature List
* Supports (theoretically) unlimited amounts of folders and (theoretically) unlimited amounts of audio files.
* Use buttons on GUI to switch folders and play the first 9 audio files.
* Click on the lists to switch folders and play any audio file.
* Use numpad keys to switch folders and play sounds no matter what application you have selected! (If event file is given)
* Multiple audio threads allowing for multiple different or same sounds to play at once!
* Ability to instantly kill all outgoing audio.

## How to run
Two methods.

A: double click on main.py and run it.

B: Open up a terminal, navigate to the soundboard folder, and run `python3 main.py`

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

### ...add more folders?
Inside of the `root_sound_folder` (Default: Sound Files, configurable in `config.ini`), there is already a folder named `1 Example`. To add an additional folder, create a folder inside the `root_sound_folder` with a name that starts with a number and ends with whatever you want, with a space separating. For example, `25 Flood Gates` or `2 Domination Sounds`.
The number that the folder is prefixed with will determine what order the folders are in inside the soundboard. For example, `25 Flood Gates` will come after `2 Domination Sounds`.

There is (theoretically) no limit to how many different folders you can have.

### ...add more audio files?
Inside of `1 Example` (which is inside the `root_sound_folder` there is already a file called `1 Example.wav`. To add an additional audio file, copy the audio file to the folder of choice inside the `root_sound_folder`, and rename it to start with a number and end with whatever you want, with a space separating. For example, `5 Double Kill.wav` or `77 Country Roads.ogg`.
The number that the file is prefixed with will determine what order the files are in inside the soundboard. For example, `77 Country Roads.ogg` will come after `5 Double Kill.wav`

There is (theoretically) no limit to how many different audio files you have, but remember that the buttons on the GUI and the keypad can only play the first 9 audio files.


## Something doesn't work!
Well, if its not listed below here, submit an issue for it and it will get fixed as soon as possible!

### No module named 'tkinter'!
If on Ubuntu, do `sudo apt install python3-tk` to get TKinter for Python3. Else, use pip to install it or find instructions for your distribution.

### My audio file doesnt play anything/console logs `Failed to open audio file`!
Pulseaudio can't play every single type of audio file. The currently tested and working audio files are `.wav` and `.ogg`. There are methods online and offline to convert `.mp3` and other audio types to the supported ones.


## "I want ____" or "How do I do ____?"

If you have any questions, concerns, ideas, etc, make an issue for it! I'm all up for recommendations on how to make this better.


## HOLY BATMAN THIS IS TEMPORARY ##
`sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0`

`sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0`
`pip3 install pycairo`
`pip3 install PyGObject`
