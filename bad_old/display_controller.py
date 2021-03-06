import tkinter as tk
from time import sleep
from bad_old.globals import global_variables, global_config
from bad_old import file_controller, input_controller
from bad_old.audio_controller import audio_logic
from bad_old.logger import log, INFO, WARNING, ERROR


def run_gui():
    """
    Easy way to get main to start running the mainloop while keeping it inside display_controller.
    Make sure all the files are read and in place before the user can do anything, then start running the window proper.
    :return: None
    """
    frame_top.refresh_files()
    window.mainloop()
    log(INFO, "create_gui", "GUI exited mainloop, shutting down!")


class FrameTopClass:
    def __init__(self):
        """
        This is where everything on the top row is created.
        """
        # Create frame and place at top.
        self.frame = tk.Frame(window)
        self.frame.grid(column=0, row=0, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.E + tk.W)
        self.frame.columnconfigure(0, weight=1)

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(column=0, row=0, sticky=tk.N + tk.W)

        # Create refresh files button.
        self.button_refresh_files = tk.Button(self.button_frame, text="Refresh Files", command=self.refresh_files)
        self.button_refresh_files.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        # Create a use event file button.
        self.button_use_event_file = tk.Button(self.button_frame, text="Use Event File", command=self.change_event_file)
        self.button_use_event_file.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        # Create a entry for entering the event file location
        self.entry_event_file = tk.Entry(self.button_frame, bd=1, width=15)
        self.entry_event_file.grid(column=2, row=0, padx=5, pady=5)
        if global_variables.input.event_file_location is None:
            self.entry_event_file.insert(0, "/dev/input/event#")
        else:
            self.entry_event_file.insert(0, global_variables.input.event_file_location)
            self.entry_event_file.config(state=tk.DISABLED)

        # Create thread count label
        thread_text = "Audio Thread Count: 0 / " + str(global_config.audio.max_audio_threads)
        self.label_thread_count = tk.Label(self.frame, text=thread_text)
        self.label_thread_count.grid(column=3, row=0, padx=5, pady=5, sticky=tk.E)

    # noinspection PyMethodMayBeStatic
    def refresh_files(self):
        """
        Have file_controller refresh the files, then have the folder_list and file_list update.
        :return: None
        """
        file_controller.refresh_files()
        if global_variables.file.locked is False:
            folder_list.update()
            file_list.update(global_variables.input.page)

    def change_event_file(self):
        """
        Create a popup window to help the user set the event file outside config.ini
        If already using the exact same event file, inform user of that.
        If there is a permission issue when accessing the file, inform the user and ask if it should attmept to resolve
        it. If the user presses No, do nothing. If the user presses yes, attempt to resolve using change_permission.
        If the file doesn't exist, Inform the user.
        If successful in setting the event file, inform the user of it and tell them how to make the change permanent.
        :return:
        """
        input_path = self.entry_event_file.get()
        if input_path == global_variables.input.event_file_location:
            # Already using the exact same event file.
            message_box = tk.Toplevel(window)
            message_box.title("Error")
            label_text = tk.Label(message_box, text="You are already using this event file!")
            label_text.grid(column=0, row=0, padx=5, pady=5)
            button_done = tk.Button(message_box, text="OK", command=message_box.destroy)
            button_done.grid(column=0, row=1, padx=5, pady=5)
        else:
            returned_value = 666
            try:
                returned_value = input_controller.event_file_checker(input_path)
            except PermissionError:
                # Permission issue.
                message_box = tk.Toplevel(window)
                message_box.title("Error")
                label_text = tk.Label(message_box, text="Permission error, attempt to resolve?")
                label_text.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
                button_yes = tk.Button(message_box, text="Yes", command=lambda: self.change_permission(input_path,
                                                                                                       message_box))
                button_yes.grid(column=0, row=1, padx=5, pady=5)
                button_no = tk.Button(message_box, text="No", command=message_box.destroy)
                button_no.grid(column=1, row=1, padx=5, pady=5)
            except FileNotFoundError:
                # File doesn't exist.
                message_box = tk.Toplevel(window)
                message_box.title("Error")
                label_text = tk.Label(message_box, text="Event file not found!")
                label_text.grid(column=0, row=0, padx=5, pady=5)
                button_done = tk.Button(message_box, text="OK", command=message_box.destroy)
                button_done.grid(column=0, row=1, padx=5, pady=5)
            if returned_value is 0:
                # Successful.
                global_variables.input.event_file_location = input_path
                message_box = tk.Toplevel(window)
                message_box.title("Event file selected")
                output_text = "Success!\n Please do the following in Config.ini to make choice persist:\n" \
                              "Change event_file_location under [INPUT] from None to: " + input_path + ""
                label_text = tk.Label(message_box, text=output_text)
                label_text.grid(column=0, row=0, padx=5, pady=5)
                button_done = tk.Button(message_box, text="OK", command=message_box.destroy)
                button_done.grid(column=0, row=1, padx=5, pady=5)
                self.entry_event_file.config(state=tk.DISABLED)
                input_controller.start_input_controller()

    def change_permission(self, input_path, message_box):
        """
        Attempt to fix permissions of the event file via input_controller.chown_event_file.
        Destroy the message box.
        Relaunch change_event_file to hopefully have it work this time.
        :param input_path: Path to event file
        :param message_box: The message box this command is being used in.
        :return:
        """
        input_controller.chown_event_file(input_path)
        message_box.destroy()
        self.change_event_file()

    def update_thread_count(self):
        """
        Update the visual thread count to reflect the thread counts from thread_count and max_audio_threads.
        :return: None
        """
        thread_text = "Audio Thread Count: " + str(global_variables.audio.thread_count) + " / " + \
                      str(global_config.audio.max_audio_threads)
        try:
            self.label_thread_count.config(text=thread_text)
        except RuntimeError:
            pass


class FolderListClass:
    def __init__(self, input_x, input_y, width):
        """
        This is where the listbox that displays all the different folders is created, with the width of the listbox
        specified by width. The placement of the frame is wherever input_x and input_y specify.
        :param input_x: Input column/X value for where the frame should be placed.
        :param input_y: Input row/Y value for where the frame should be placed.
        :param width: Width of the listbox.
        """
        # Create labelframe and adjust weights
        self.labelframe = tk.LabelFrame(window, text="Folders", padx=5, pady=5)
        self.labelframe.grid(column=input_x, row=input_y, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.labelframe.columnconfigure(0, weight=1)
        self.labelframe.rowconfigure(0, weight=1)

        # Create, add a bind, and place the listbox that will contain the names of all the folders.
        self.listbox = tk.Listbox(self.labelframe, width=width)
        self.listbox.bind("<ButtonRelease-1>", self.listbox_select)
        self.listbox.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create and bind a vertical scrollbar to the listbox above.
        self.scrollbar_vertical = tk.Scrollbar(self.labelframe, orient="vertical")
        self.scrollbar_vertical.config(command=self.listbox.yview)
        self.scrollbar_vertical.grid(column=1, row=0, sticky=tk.N + tk.S + tk.E)
        self.listbox.config(yscrollcommand=self.scrollbar_vertical.set)

        # Create and bind a horizontal scrollbar to the listbox above.
        self.scrollbar_horizontal = tk.Scrollbar(self.labelframe, orient="horizontal")
        self.scrollbar_horizontal.config(command=self.listbox.xview)
        self.scrollbar_horizontal.grid(column=0, row=1, sticky=tk.S + tk.E + tk.W)
        self.listbox.config(xscrollcommand=self.scrollbar_horizontal.set)

    def listbox_select(self, dummy):
        """
        Set the page equal to the selection index, then update the file list with the new page.
        :param dummy: Dummy variable, not used.
        :return: None
        """
        if len(self.listbox.curselection()) > 0:
            global_variables.input.page = self.listbox.curselection()[0]
            file_list.update(global_variables.input.page)

    def update(self):
        """
        Update with the names of all the folders.
        :return: None
        """
        output_list = global_variables.file.folder_names
        self.listbox_fill(output_list)

    def listbox_fill(self, input_list):
        """
        Quickly update the listbox with an input list. Each string in the list will be its own entry.
        :param input_list: Input list to fill the listbox with.
        :return: None
        """
        self.listbox.delete(0, tk.END)
        for item in input_list:
            self.listbox.insert(tk.END, item)


class PlayButtonsClass:
    def __init__(self, input_x, input_y):
        """
        This is where the buttons that changes pages and plays audio files are created. The placement of the frame is
        wherever input_x and input_y specify.
        :param input_x: Input column/X value for where the frame should be placed.
        :param input_y: Input row/Y value for where the frame should be placed.
        """
        # Create the labelframe that will contain all the buttons
        self.labelframe = tk.LabelFrame(window, text="Play Buttons", padx=5, pady=5)
        self.labelframe.grid(column=input_x, row=input_y, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create the Minus Button that will go back a folder.
        self.button_minus = tk.Button(self.labelframe, text=" - Folder", width=7, command=self.back_page)
        self.button_minus.grid(column=0, row=0, padx=5, pady=5)

        # Create the Plus button that will go forward a folder.
        self.button_plus = tk.Button(self.labelframe, text="+ Folder", width=7, command=self.forward_page)
        self.button_plus.grid(column=2, row=0, padx=5, pady=5)

        self.audio_button = []
        for i in range(10):
            self.audio_button.append(self.AudioButtonClass(self.labelframe, i))
        # self.test = self.AudioButtonClass(self.labelframe, 2)

    class AudioButtonClass:
        def __init__(self, input_labelframe, input_number):
            """
            This is where the audio buttons that play sounds are created. Placement is based on input_number, and the
            frame the button is put in is based on input_labelframe.
            :param input_labelframe: Input frame where the button will be placed.
            :param input_number: Input integer that the button will correspond to.
            """
            self.number = input_number
            # 0 is an exception, so build a special case for that. Default to normal for 1-9, and error for >9.
            if self.number is 0:
                name = "Kill Audio 0"
                placement = [0, 4]
            elif 0 < self.number < 10:
                name = "Audio " + str(self.number)
                # Get placement of the X coordinate by doing math to get where on the keypad the number is.
                placement_x = (self.number - 1) % 3
                # Get placement of the Y coordinate by doing math to get where on the keypad the number is.
                placement_y = 3 - (self.number - 1) // 3
                placement = [placement_x, placement_y]
            else:
                raise SyntaxError
            # Finally create the button.
            self.button = tk.Button(input_labelframe, text=name, width=7, command=self.play_audio)
            self.button.grid(column=placement[0], row=placement[1])

        def play_audio(self):
            """
            Used exclusively for the audio buttons.
            Get what number the button is.
            If the button is not 0, attempt to play an audio file determined by the current page and number of button
            pressed.
            Else if the button is 0, kill all running audio processes.
            Else, do nothing as nothing should hit the else.
            :return: None
            """
            if self.number is not 0:
                audio_logic(global_variables.input.page, self.number - 1)
            elif self.number is 0:
                global_variables.audio.kill_audio = True
                sleep(global_config.audio.polling_rate)
                global_variables.audio.kill_audio = False
            else:
                log(WARNING, "play_audio", "Invalid button \"" + self.number + "\" attempted to play a sound?")
                pass

    # noinspection PyMethodMayBeStatic
    def back_page(self):
        """
        Decrement the page by one.
        If that makes the page number less than one, reset it to the highest valid value. This essentially makes a
        wrap-around effect.
        :return: None
        """
        global_variables.input.page -= 1
        if global_variables.input.page < 0:
            global_variables.input.page = len(global_variables.file.folder_names) - 1

        file_list.update(global_variables.input.page)

    # noinspection PyMethodMayBeStatic
    def forward_page(self):
        """
        Increment the page by one.
        If that makes the page number greater than the highest valid value, reset it to 0. This essentially makes a
        wrap-around effect.
        :return:
        """
        global_variables.input.page += 1
        if global_variables.input.page >= len(global_variables.file.folder_names):
            global_variables.input.page = 0
        file_list.update(global_variables.input.page)


class FileListClass:
    def __init__(self, input_x, input_y, width):
        """
        This is where the listbox that displays all the different audio files is created. The placement is wherever
        input_x and input_y specify.
        :param input_x: Input column/X value for where the frame should be placed.
        :param input_y: Input row/Y value for where the frame should be placed.
        :param width: Width of the listbox.
        """
        # Create labelframe and adjust weights
        self.labelframe = tk.LabelFrame(window, text="Files", padx=5, pady=5)
        self.labelframe.grid(column=input_x, row=input_y, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.labelframe.columnconfigure(0, weight=1)
        self.labelframe.rowconfigure(0, weight=1)

        # Create, add a bind, and place the listbox that will contain the names of all the files.
        self.listbox = tk.Listbox(self.labelframe, width=width)
        self.listbox.bind("<ButtonRelease-1>", self.listbox_select)

        self.listbox.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create and bind a vertical scrollbar to the listbox above.
        self.scrollbar_vertical = tk.Scrollbar(self.labelframe, orient="vertical")
        self.scrollbar_vertical.config(command=self.listbox.yview)
        self.scrollbar_vertical.grid(column=1, row=0, sticky=tk.N + tk.S + tk.E)
        self.listbox.config(yscrollcommand=self.scrollbar_vertical.set)

        # Create and bind a horizontal scrollbar to the listbox above.
        self.scrollbar_horizontal = tk.Scrollbar(self.labelframe, orient="horizontal")
        self.scrollbar_horizontal.config(command=self.listbox.xview)
        self.scrollbar_horizontal.grid(column=0, row=1, sticky=tk.S + tk.E + tk.W)
        self.listbox.config(xscrollcommand=self.scrollbar_horizontal.set)

    def listbox_select(self, dummy):
        """
        Attempt to play the audio file selected in the listbox.
        :param dummy: Dummy variable, not used.
        :return: None
        """
        if len(self.listbox.curselection()) > 0:
            index = self.listbox.curselection()[0]
            audio_logic(global_variables.input.page, index)

    def update(self, input_page):
        """
        Updates the list of file names in the listbox to match a given page.
        :param input_page: Integer representing a valid index value in file_names.
        :return:
        """
        output_list = global_variables.file.file_names[input_page]
        self.listbox_fill(output_list)

    def listbox_fill(self, input_list):
        """
        Quickly update the listbox with an input list. Each string in the list will be its own entry.
        :param input_list: Input list to fill the listbox with.
        :return: None
        """
        self.listbox.delete(0, tk.END)
        for item in input_list:
            self.listbox.insert(tk.END, item)


def display_terminal_output():
    """
    Function to display_terminal_outout. Because this is not implemented, log an error and raise an exception.
    :return: None
    """
    log(ERROR, "display_terminal_output", "NO TERMINAL OUTPUT SUPPORTED, SWITCH use_gui IN Config.ini FROM False TO "
                                          "True!")
    raise NotImplementedError


if global_config.main.use_gui is True:
    """
    If the use_gui value is True, setup the GUI to let the main thread run it.
    """
    window = tk.Tk()
    log(INFO, "DisplayController", "Initial GUI created.")

    log(INFO, "DisplayController", "Populating GUI.")
    window.title("Python Linux Soundboard")

    # Create the top buttons
    frame_top = FrameTopClass()

    # Create the folder list at coordinates 0, 1 and allow stretching.
    folder_list = FolderListClass(0, 1, 15)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    # Create the play buttons at coordinates 1, 1.
    play_buttons = PlayButtonsClass(1, 1)

    # Create the file list at coordinates 2, 1 and allow stretching
    file_list = FileListClass(2, 1, 15)
    window.columnconfigure(2, weight=1)
