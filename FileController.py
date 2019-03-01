from os import listdir
from Globals import global_variables
from Config import global_config
from Logger import log, INFO, WARNING  # , ERROR


def refresh_files():
    log(INFO, "refresh_files", "Starting refresh.")
    if global_variables.file.locked is False:
        # First, lock and clear all folder names, file names, and file paths.
        global_variables.file.locked = True
        global_variables.file.folder_names.clear()
        global_variables.file.file_names.clear()
        global_variables.file.file_paths.clear()

        # Get a list of folders, and add the names to folder_names.
        folder_list = get_item_list(global_config.root_sound_folder)
        for folder in folder_list:
            global_variables.file.folder_names.append(folder)

            # Get a list of files in the folder, add the name and path to seperate lists, and add the name list and path
            # list to file_names and file_paths respectively.
            file_list = get_item_list(global_config.root_sound_folder + "/" + folder)
            pre_file_names = []
            pre_file_paths = []
            for file in file_list:
                pre_file_names.append(file)
                pre_file_paths.append(global_config.root_sound_folder + "/" + folder + "/" + file)
            global_variables.file.file_names.append(pre_file_names)
            global_variables.file.file_paths.append(pre_file_paths)

        # Since the folder/file names/paths are no longer being written to, unlock them.
        global_variables.file.locked = False
        log(INFO, "refresh_files", "Ended refresh.")
    else:
        log(WARNING, "refresh_files", "Files are locked, is a refresh already occurring?")


def get_prefix(input_string):
    done = False
    prefix_length = 0
    prefix = None
    while not done:
        if input_string[prefix_length].isdigit() is True:
            prefix_length += 1
        else:
            done = True
    if input_string[prefix_length] is " ":
        prefix = int(input_string[:prefix_length])
    else:
        pass
    return prefix


def get_item_list(root_folder):
    pre_item_list = listdir(root_folder)
    post_item_list = []

    # Get the count of all prefixes, in case there's a prefix-less item
    prefix_count = 0
    for item in pre_item_list:
        prefix = get_prefix(item)
        if prefix is None:
            pass
        else:
            prefix_count += 1
    # Add the folders in numeric order.
    counter = 0
    while len(post_item_list) < prefix_count:
        for item in pre_item_list:
            prefix = get_prefix(item)
            if prefix is None:
                pass
            else:
                if prefix == counter:
                    post_item_list.append(item)
                else:
                    pass
        counter += 1
    return post_item_list
