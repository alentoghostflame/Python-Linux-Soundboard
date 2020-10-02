import subprocess
import os


def get_file_list():
    os.makedirs("Sound Files", exist_ok=True)

    folder_list = os.listdir("Sound Files")
    folder_list.sort()
    sound_folder_list = []
    folder_name_list = []
    for folder in folder_list:
        sound_folder_list.append(SoundFolder(folder, os.listdir("Sound Files/{}".format(folder))))
        folder_name_list.append(folder)
    return sound_folder_list, folder_name_list


class SoundFolder:
    def __init__(self, name: str, content: list):
        self.name: str = name
        self.content: list = content
        self.content.sort()

    def get_path_for_index(self, index: int):
        return "{}/{}".format(self.name, self.content[index]).replace(" ", "\\ ")


class AudioThreads:
    def __init__(self, max_threads: int):
        self.threads: set = set()
        self.max_threads = max_threads

    def clean_threads(self):
        trash_threads = set()
        for thread in self.threads:
            if thread.poll() is not None:
                trash_threads.add(thread)
        self.threads.difference_update(trash_threads)

    def play_sound(self, sound_folder: SoundFolder, index: int):
        self.clean_threads()
        if len(sound_folder.content) > index and len(self.threads) < self.max_threads:
            path = "Sound\\ Files/{}".format(sound_folder.get_path_for_index(index))
            thread = subprocess.Popen("exec paplay {}".format(path), shell=True, stdout=subprocess.PIPE)
            self.threads.add(thread)

    def kill_sounds(self):
        for thread in self.threads:
            thread.terminate()
        self.threads = set()

    def get_thread_count(self):
        self.clean_threads()
        return len(self.threads)
