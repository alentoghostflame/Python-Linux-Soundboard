# Python-Linux-Soundboard
I couldn't find any soundboards compatible with Linux that fit my standards, so I made my own that uses the numpad.


## Requirements
- `PyYaml` for easy reading and writing of configuration file(s).
- `TKInter` to create the interface. On Ubuntu, do `sudo apt install python3-tk` to install it.
- `PyOpenAL` to play sounds.
- `PyOgg` to allow `PyOpenAL` to play `.ogg` files.

Two soft requirements would be `pavucontrol` (PulseAudio Volume Control, to control where output is redirected) and the
sister project to this, the 
[Pulseaudio-Loopback-Tool](https://github.com/alentoghostflame/Python-Pulseaudio-Loopback-Tool). (to create loopbacks,
null sinks, and remapped sources)

Install `pavucontrol` on Ubuntu by doing `sudo apt install pavucontrol`  
Install [Pulseaudio-Loopback-Tool](https://github.com/alentoghostflame/Python-Pulseaudio-Loopback-Tool) by clicking the
link and downloading that project.

## Quick Feature List
* Supports (theoretically) unlimited amounts of folders and (theoretically) unlimited amounts of audio files.
* Use buttons on the GUI to switch folders and play the first 9 mapped audio files.
* Click on the lists to switch folders and play any audio file.
* Use numpad keys to switch folders and play sounds no matter what application you have selected!
* Multiple audio threads allowing for multiple different or same sounds to play at once!
* Ability to instantly kill all outgoing audio.

## Setting up for first use
Clean way: follow steps normally.  
Dirty way: Do step 1, skip to step 4, and follow steps normally from then.

1. Download this repository and unzip if need be.
2. In the repository folder, perform `python3 -m venv venv` to make a Virtual Environment.
3. Activate it using `source venv/bin/activate`
4. Install requirements via `pip3 install -r requirements.txt`
    - If it fails to install, try `pip3 install wheel && pip3 install --force-reinstall -r requirements.txt`
5. Run the soundboard either by doing `python3 start.py` or `./start.py`

### Dirty vs Clean
The "Clean" installation keeps the requirements of this project away from your local Python 3 installation, making sure
that these requirements don't interfere with the requirements of your other Python programs. The cost is that more work
has to be done to start up the project, requiring you to `source venv/bin/activate` before starting the soundboard up.

The "Dirty" installation has the requirements installed into your local Python 3 installation, possibly interfering with
other Python programs. The upside is that it is easier to start the project, and double clicking `start.py` to start the
soundboard is easily possible.

## How to...
Small list of "How to do this common thing", if you either have a question or found something that you think belongs
here, make an issue for it and I'll probably add it!

### ...actually use the soundboard?
Three different ways, actually:
1. Click the sub-folder on the left that contains the sound that you want to play, then click the sound on the right.
2. Use the buttons to go back and forth between folders, and play sounds that are mapped to those keys.
3. Use numpad controls to simulate pressing the buttons.

### ...make numpad controls work?
Top middle of the soundboard is a pulldown. In the pulldown is all the input devices the soundboard found in
`/dev/input/by-id`. Select the keyboard that you want the soundboard to listen to, press the "Use Event File" button, 
and the numpad on the keyboard should now trigger the soundboard buttons.

### ...increase the maximum audio thread count?
Ten not enough for you? Edit `soundboard_config.yaml` with any text editor and change `max_sounds` from 10 to whatever
number you want. Increasing this number will not decrease performance, it's playing many sounds at once that will.

### ...make applications listen to this?
Using `pavucontrol` you can set the soundboard to output to any available sink, and sinks can be created by PALT. 
(PulseAudio-Looback-Tool)
Ideally, you'd have the following basic setup:
1. Using PALT: Create a sink called "Audible_Layer"
2. PALT: Remap "Audible_Layer" to "Output_Mic"
3. PALT: Loopback "Audible_Layer" to your speakers/headphones, so you can hear the soundboard as well.
4. Using `pavucontrol`: Set your recording application to use "Output_Mic"

### ...change the root folder?
If you haven't run the soundboard yet, run it once to create the config file.  
Edit `soundboard_config.yaml` with any text editor and change "Sound Files" to the path of the desired root folder, 
either relative to where you are executing `start.py` or absolute.

### ...add more sub-folders?
Simply add more folders in the root folder! It's alphabetically sorted in the list, so adding 1, 2, 3, etc. to the
beginning of the folder name will force it to go in that order.  
There is (theoretically) no limit to how many different folders you can have.

### ...add more audio files?
Put audio files into into the sub-folders. Just like the folders, it's alphabetically sorted in the list.  
Again, there is (theoretically) no limit to how many different audio files you can have.

### ...map an audio file to a button?
Rename the sound file to have a number and a space at the beginning of the filename, with the number being what
number button you want it mapped to. If you want a sound called `hey.ogg` mapped to the 3 button, rename it to 
`3 hey.ogg`   
Renaming it to `3hey.ogg` or `3_hey.ogg` will not work, the space is required.  
If multiple files start with the same number, the soundboard will pick the first one it finds.

## Something doesn't work!
Well, if its not listed below here, submit an issue for it and it will get fixed as soon as possible!

### I can't change the output device for this in `pavucontrol`!
It's a configuration setting in OpenAL, edit the config file and change `allow-moves` to true.
For example:
1. `sudo nano /etc/openal/alsoft.conf`
2. Control + w, `allow-m`, press enter.
3. Find `#allow-moves = false` and change it to `allow-moves = true`
4. Control + x, y, enter.

The change should take effect immediately, but may require a restart of the soundboard.

### No module named 'tkinter'!
If on Ubuntu, do `sudo apt install python3-tk` to get TKinter for Python3. Else, use pip to install it or find
instructions for your distribution.

### My audio file doesn't show up/console logs `Rejected file <file path here>`!
As far as I know, OpenAL supports `.wav`, but because of `pyogg` it also supports `.ogg` files. The soundboard will
reject all non-`.wav`/`.ogg` files it finds. If OpenAL can run more than those files, make an issue for it and I'll
update it.  
If you are impatient, edit `SOUND_FILE_EXTENSIONS` in `soundboard/storage_module/storage_manager.py` and add
the file format there to make it show up.

## "I want ____" or "How do I do ____?"

If you have any questions, concerns, ideas, etc, make an issue for it! I'm all up for recommendations on how to make this better.
