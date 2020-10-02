import program_logic
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class SoundboardBase(Gtk.Window):
    def __init__(self):
        # Gtk.Window.__init__(self, title="Python Linux Soundboard")
        super().__init__(title="Python Linux Soundboard")
        self.window_grid = WindowGrid()
        self.add(self.window_grid)

        self.sound_folder_list: list = []
        self.folder_name_list: list = []
        self.folder_count: int = 0
        self.current_folder: int = 0

        self.audio_threads = program_logic.AudioThreads(10)
        GObject.timeout_add(1000, self.refresh_thread_count)

    def setup_run(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.refresh(refresh_files=True)
        Gtk.main()

    def refresh(self, refresh_files: bool = False):
        if refresh_files:
            self.sound_folder_list, self.folder_name_list = program_logic.get_file_list()
            self.folder_count = len(self.folder_name_list)
            self.window_grid.folder_list.delete_text_all()
            self.window_grid.folder_list.insert_text_bulk(self.folder_name_list)

            self.current_folder = 0
            self.window_grid.change_selected_folder(self.current_folder)

        self.window_grid.file_list.delete_text_all()
        self.window_grid.file_list.insert_text_bulk(self.sound_folder_list[self.current_folder].content)

    def get_folder_count(self):
        return self.folder_count

    def set_folder_count(self, count: int):
        self.folder_count = count

    def get_current_folder(self):
        return self.current_folder

    def change_current_folder(self, change: int):
        self.current_folder += change
        if self.current_folder < 0:
            self.current_folder = self.folder_count - 1
        elif self.current_folder >= self.folder_count:
            self.current_folder = 0

    def set_current_folder(self, index: int):
        self.current_folder = index

    def play_audio_file(self, index: int):
        self.audio_threads.play_sound(self.sound_folder_list[self.current_folder], index)

    def kill_audio(self):
        self.audio_threads.kill_sounds()

    def get_audio_thread_count(self):
        return self.audio_threads.get_thread_count()

    def refresh_thread_count(self):
        self.window_grid.top_bar.audio_thread_count.refresh_thread_count(self.audio_threads)
        return True


class WindowGrid(Gtk.Grid):
    def __init__(self):
        super().__init__()

        self.top_bar = TopBar()
        self.attach(self.top_bar, 0, 0, 3, 1)

        self.folder_list = FolderList()
        self.attach(self.folder_list, 0, 1, 1, 1)
        self.central_numpad = CentralNumPad()
        self.attach(self.central_numpad, 1, 1, 1, 1)
        self.file_list = FileList()
        self.attach(self.file_list, 2, 1, 1, 1)

    def get_folder_count(self):
        return self.get_parent().get_folder_count()

    def set_folder_count(self, count: int):
        return self.get_parent().set_folder_count(count)

    def get_current_folder(self):
        return self.get_parent().get_current_folder()

    def change_current_folder(self, change: int):
        self.get_parent().change_current_folder(change)
        current_folder = self.get_parent().get_current_folder()
        # self.folder_list.select_row(current_folder)
        self.change_selected_folder(current_folder)

    def set_current_folder(self, index: int):
        self.get_parent().set_current_folder(index)

    def change_selected_folder(self, row: int):
        self.folder_list.select_row(row)

    def refresh(self, refresh_files=False):
        self.get_parent().refresh(refresh_files=refresh_files)

    def play_audio_file(self, index: int):
        self.get_parent().play_audio_file(index)
        thread_count = self.get_parent().get_audio_thread_count()
        self.top_bar.audio_thread_count.set_thread_count(thread_count)

    def kill_audio(self):
        self.get_parent().kill_audio()


class TopBar(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.refresh_button = Gtk.Button(label="Refresh Files", expand=True, margin=2)
        self.refresh_button.connect("clicked", self.refresh_clicked)
        self.pack_start(self.refresh_button, True, True, 0)

        self.use_file_button = Gtk.Button(label="Use Event File", expand=True, margin=2)
        self.use_file_button.connect("clicked", self.use_file_clicked)
        self.pack_start(self.use_file_button, True, True, 0)

        self.file_chooser = Gtk.FileChooserButton(expand=True, margin=2)
        self.file_chooser.connect("file-set", self.file_chosen)
        self.pack_start(self.file_chooser, True, True, 0)

        self.audio_thread_count = AudioThreadCount()
        self.pack_end(self.audio_thread_count, True, True, 0)

    def refresh_clicked(self, widget):
        print("FIXME: Refresh button clicked.")
        self.get_parent().refresh(refresh_files=True)

    def file_chosen(self, widget):
        print("FIXME: File chosen: {}")

    def use_file_clicked(self, widget):
        print("FIXME: Use file button clicked.")


class AudioThreadCount(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.STYLE_CLASS_VERTICAL)
        self.max_thread_count = 10

        self.level_bar = Gtk.LevelBar(expand=True, margin=2)
        self.pack_start(self.level_bar, True, True, 0)

        self.label = Gtk.Label(label="Audio Thread Count: 0 / {}".format(self.max_thread_count), expand=True, margin=2)
        self.pack_start(self.label, True, True, 0)

    def set_max_thread_count(self, max_threads: int):
        print("FIXME: Max thread count set to {}".format(max_threads))
        self.max_thread_count = max_threads

    def set_thread_count(self, thread_count: int):
        print("FIXME: Thread count set to {}".format(thread_count))
        self.level_bar.set_value(thread_count / self.max_thread_count)
        self.label.set_text("Audio Thread Count: {} / {}".format(thread_count, self.max_thread_count))

    def refresh_thread_count(self, audio_threads: program_logic.AudioThreads):
        print("FIXME: Refreshing thread count.")
        thread_count = audio_threads.get_thread_count()
        self.level_bar.set_value(thread_count / self.max_thread_count)
        self.label.set_text("Audio Thread Count: {} / {}".format(thread_count, self.max_thread_count))


class FolderList(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__(expand=True)
        self.listbox = Gtk.ListBox()
        self.add(self.listbox)
        self.listbox.connect("row-activated", self.on_click)

    def on_click(self, widget, row):
        print("FIXME: Folder pressed: {}".format(row.name))
        # print(row.get_index())
        self.get_parent().set_current_folder(row.get_index())
        self.get_parent().refresh()

    def insert_text_bulk(self, text_list: list):
        print("inserting bulk text {}".format(text_list))
        for text in text_list:
            self.listbox.add(ListBoxRowLabel(text))
        self.listbox.show_all()

    def insert_text(self, text: str):
        print("inserting text {}".format(text))
        self.listbox.add(ListBoxRowLabel(text))
        self.listbox.show_all()

    def delete_text_all(self):
        print("FIXME: Deleting all folders in list.")
        for child in self.listbox.get_children():
            self.listbox.remove(child)

    def select_row(self, row: int):
        rows = self.listbox.get_children()
        self.listbox.select_row(rows[row])
        self.listbox.show_all()


class FileList(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__(expand=True)
        self.listbox = Gtk.ListBox()
        self.add(self.listbox)
        self.listbox.connect("row-activated", self.on_click)

    def on_click(self, widget, row):
        print("FIXME: File pressed: {}".format(row.name))
        self.get_parent().play_audio_file(row.get_index())

    def insert_text_bulk(self, text_list: list):
        print("inserting bulk text {}".format(text_list))
        for text in text_list:
            self.listbox.add(ListBoxRowLabel(text))
        self.listbox.show_all()

    def insert_text(self, text: str):
        print("inserting text {}".format(text))
        self.listbox.add(ListBoxRowLabel(text))
        self.listbox.show_all()

    def delete_text_all(self):
        print("FIXME: Deleting all files in list.")
        for child in self.listbox.get_children():
            self.listbox.remove(child)

    def select_row(self, row: int):
        self.listbox.select_row(row)


class ListBoxRowLabel(Gtk.ListBoxRow):
    def __init__(self, text: str):
        super().__init__()
        self.label = Gtk.Label(label=text)
        self.add(self.label)
        self.name = text


class CentralNumPad(Gtk.Grid):
    def __init__(self):
        super().__init__(margin=10)
        self.vexpand = True
        self.button_7 = NumPadButton("Audio 7", self.num_pressed, 7)
        self.attach(self.button_7, 0, 1, 1, 1)
        self.button_8 = NumPadButton("Audio 8", self.num_pressed, 8)
        self.attach(self.button_8, 1, 1, 1, 1)
        self.button_9 = NumPadButton("Audio 9", self.num_pressed, 9)
        self.attach(self.button_9, 2, 1, 1, 1)
        self.button_4 = NumPadButton("Audio 4", self.num_pressed, 4)
        self.attach(self.button_4, 0, 2, 1, 1)
        self.button_5 = NumPadButton("Audio 5", self.num_pressed, 5)
        self.attach(self.button_5, 1, 2, 1, 1)
        self.button_6 = NumPadButton("Audio 6", self.num_pressed, 6)
        self.attach(self.button_6, 2, 2, 1, 1)
        self.button_1 = NumPadButton("Audio 1", self.num_pressed, 1)
        self.attach(self.button_1, 0, 3, 1, 1)
        self.button_2 = NumPadButton("Audio 2", self.num_pressed, 2)
        self.attach(self.button_2, 1, 3, 1, 1)
        self.button_3 = NumPadButton("Audio 3", self.num_pressed, 3)
        self.attach(self.button_3, 2, 3, 1, 1)
        self.button_minus = NumPadButton("Folder -", self.back_page)
        self.attach(self.button_minus, 0, 0, 1, 1)
        self.button_0 = NumPadButton("Kill Audio 0", self.kill_audio)
        self.attach(self.button_0, 0, 4, 1, 1)
        self.button_plus = NumPadButton("Folder +", self.next_page)
        self.attach(self.button_plus, 2, 0, 1, 1)

    def num_pressed(self, widget):
        print("FIXME: Button number {} pressed.".format(widget.number))
        self.get_parent().play_audio_file(widget.number - 1)

    def next_page(self, widget):
        print("FIXME: Button next page pressed.")
        self.get_parent().change_current_folder(1)
        self.get_parent().refresh()

    def back_page(self, widget):
        print("FIXME: Button back page pressed.")
        self.get_parent().change_current_folder(-1)
        self.get_parent().refresh()

    def kill_audio(self, widget):
        print("FIXME: Kill audio button pressed.")
        self.get_parent().kill_audio()


class NumPadButton(Gtk.Button):
    def __init__(self, label: str, command, number=None):
        super().__init__(label=label, expand=True, margin=2)
        self.number = number
        self.connect("clicked", command)


# win = Gtk.Window()
# win = SoundboardBase()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()

# window = SoundboardBase()
# window.setup_run()




