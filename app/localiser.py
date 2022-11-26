from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from midi_processing.midi_to_notes import Note, get_notes
from midi_processing.convert_to_audio import run

import os


"""
Standard button sizes (in pixels)
"""
button_width = 100
button_height = 50

data_folder = "../data/"


def get_notes_in_song(song):
    """
    Gets a list of Note objects in repr format

    Parameters
    ----------
    song : A string indicating the text file of the song

    Returns
    -------
    A list of strings
    """

    with open(song) as f:
        lines = f.readlines()

    return lines


class SongButton(Button):
    """
    Song button class
    """

    def __init__(self, file_name, **kwargs):
        """
        The constructor for a song button. This is the with the name of a song, in the list of songs which will
        be displayed on the home screen of the app

        The background is set to gray (RGBa), the relative height for the button is disabled
        and set to 40 pixels, but set to 50% of the window's width. Its text displays the song name

        Parameters
        ----------
        file_name : A string indicating the file name of the song
        kwargs : Arguments of the super that can be overridden
        """
        super(SongButton, self).__init__(**kwargs)

        self.background_color = [1, 1, 1, 1]
        self.size_hint = (0.5, None)
        self.height = 40

        self.file_name = file_name

    def on_press(self):
        """
        Listens for a press event. When the user presses this button, it creates a new MIDI sheet with the notes in the
        song. The screen then transitions to the left and opens the MIDI sheet. The current screen shown to the user
        is then updated to show the MIDI sheet

        Returns
        -------
        void
        """
        App.get_running_app().root.add_widget(MidiSheet(name=self.file_name))
        App.get_running_app().root.transition.direction = "left"
        App.get_running_app().root.current = self.file_name


class BackButton(Button):
    """
    Class for the back button
    """
    def __init__(self, screen_instance, **kwargs):
        """
        Constructor for the Back button. This button is displayed on every MIDI sheet to take the user back to the
        home screen

        The background is set to gray (RGBa), the relative size is disabled, and the size (pixels) is set to the
        standard button size

        Parameters
        ----------
        screen_instance : A MIDI sheet object
        kwargs : Arguments of the super that can be overridden
        """
        super(BackButton, self).__init__(**kwargs)

        self.background_color = [1, 1, 1, 1]
        self.size_hint = (None, None)
        self.size = (button_width, button_height)
        self.text = "Back"

        self.screen_instance = screen_instance

    def on_press(self):
        """
        Listens for a press event. When the user presses this button, it removes the instance of the MIDI sheet from
        the app (which saves memory), transitions the screen to the right and sets the current screen to the home
        screen

        Returns
        -------
        void
        """
        App.get_running_app().root.remove_widget(self.screen_instance)
        App.get_running_app().root.transition.direction = "right"
        App.get_running_app().root.current = "home"


class MidiButton(Button):
    """
    Class for the MIDI button
    """
    def __init__(self, midi_note, first_note, total_duration, **kwargs):
        """
        Constructor of a MIDI button. These buttons are also indications of which notes the user must play, with
        an approximation for the amount of time they should play the note for

        The background is set to gray (RGBa) and the relative size is disabled

        The width of the button is proportional to its played duration. Height of the button is standard

        Parameters
        ----------
        midi_note : A Note object
        first_note : An integer indicating the first played MIDI note number in a song
        total_duration : A float indicating the total duration of the song
        kwargs : Arguments of the super that can be overridden
        """
        super(MidiButton, self).__init__(**kwargs)

        self.background_color = [1, 1, 1, 1]
        self.size_hint = (None, None)

        self.size = (button_width * midi_note.played_time, button_height)

        # Small distance from x = 0
        buffer_x = 100

        # Layout width is the number of seconds in the songs + 2 (where 2 is buffer) * standard button width
        layout_width = (total_duration + 2) * button_width

        # The centre of the button is the ratio of the button's start time out of the whole song duration times
        # the width of the layout
        x = (midi_note.start_time/total_duration) * layout_width

        # The amount of pixels above or below the first button in the song
        delta_y = ((midi_note.note - first_note)/first_note) * Window.height

        self.pos = (buffer_x + x, delta_y + Window.height/2)

        self.text = midi_note.name

        self.start_time = midi_note.start_time
        self.end_time = midi_note.end_time
        self.played_time = midi_note.played_time

    def on_press(self):
        """
        When the button is pressed, it will turn green

        Returns
        -------
        void
        """
        self.background_color = [0, 1, 0, 1]

    def on_release(self):
        """
        When the button is released, it will return to grey

        Returns
        -------
        void
        """
        self.background_color = [1, 1, 1, 1]


class Home(Screen):
    """
    Class for the home screen of the app
    """

    def __init__(self, **kwargs):
        """
        Constructor for the home screen

        Creates a scrollable window, the same size as the window. Creates a gridlayout with 1 column and as many rows
        as required (a list). The processed MIDI files should produce a text file which can be opened to create a
        MIDI sheet

        Parameters
        ----------
        kwargs : Arguments for the super class
        """
        super(Home, self).__init__(**kwargs)

        screen = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)

        # Filters text files
        songs = [x for x in os.listdir(data_folder) if ".txt" in x]

        for song in songs:
            name = song.replace("_", " ").replace(".txt", "")

            layout.add_widget(SongButton(song, text=name))

        screen.add_widget(layout)

        self.add_widget(screen)


class MidiLayout(RelativeLayout):
    """
    Class for the MidiLayout. This layout will display all the MIDI notes in a song
    """

    def __init__(self, midi_buttons, **kwargs):
        """
        Constructor for the MidiLayout. The width of this layout will be proportional to the duration of a song.
        10 seconds are added as a buffer for the width

        Parameters
        ----------
        midi_buttons : A list of MidiButton objects
        kwargs : Arguments of the super
        """
        super(MidiLayout, self).__init__(**kwargs)

        self.size_hint = (None, None)

        self.size = ((midi_buttons[-1].end_time + 10) * button_width, Window.height)

        for button in midi_buttons:
            self.add_widget(button)


class MidiSheet(Screen):
    """
    Class for the MidiSheet screen. This screen will contain the MidiLayout and a scrolling window
    """

    def __init__(self, **kwargs):
        """
        Constructor of the MidiSheet. First creates a scrolling window. Then all the notes from a song's
        text file are split by a regex and this list is used to create Note objects. These note objects will be used
        to create MidiButton's, which will be added to the MidiLayout

        Parameters
        ----------
        kwargs : Arguments of the super
        """
        super(MidiSheet, self).__init__(**kwargs)

        screen = ScrollView(size_hint=(None, None), size=(Window.width, Window.height), do_scroll_x=True, do_scroll_y=False)

        self.notes = get_notes_in_song("../data/" + self.name)

        first_note = int(self.notes[0].split(":")[0])
        total_duration = float(self.notes[-1].split(":")[4])

        self.midi_buttons = []

        for note in self.notes:
            strings = note.split(":")
            midi_note = Note(int(strings[0]), float(strings[3]), float(strings[4]), float(strings[5]))
            self.midi_buttons.append(MidiButton(midi_note, first_note, total_duration))

        layout = MidiLayout(self.midi_buttons)

        layout.add_widget(BackButton(self))
        screen.add_widget(layout)

        self.add_widget(screen)


class Localiser(App):
    """
    Class for the localiser app
    """

    def build(self):
        """
        Builds the app. Before doing so, it checks if the midi files have their corresponding .wav and .txt files - if
        not, it will create them

        Returns
        -------
        A screen manager object, containing the home screen
        """

        for file in os.listdir(data_folder):

            if ".mid" in file:

                txt_file = file.replace(".mid", ".txt")
                wav_file = file.replace(".mid", ".wav")

                if os.path.exists(data_folder+txt_file) and os.path.exists(data_folder+wav_file):
                    continue

                # Convert to audio
                run(data_folder+file, ".wav", sound_font="../sound_fonts/Roland_SC-55.sf2")

                # Create .txt file with notes
                get_notes(data_folder+file)

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Home(name="home"))

        return sm




