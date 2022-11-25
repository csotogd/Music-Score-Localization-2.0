from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.animation import Animation
from kivy.effects.scroll import ScrollEffect

from midi_processing.midi_to_notes import Note

import os


def get_notes_in_song(song):

    with open(song) as f:
        lines = f.readlines()

    return lines


class SongButton(Button):

    def __init__(self, file_name, **kwargs):
        super(SongButton, self).__init__(**kwargs)

        self.background_color = [0, 0, 0, 0]
        self.size_hint = (0.5, None)
        self.height = 40

        self.file_name = file_name

    def on_press(self):
        App.get_running_app().root.add_widget(MidiSheet(name=self.file_name))
        App.get_running_app().root.transition.direction = "left"
        App.get_running_app().root.current = self.file_name


class BackButton(Button):
    def __init__(self, screen_instance, **kwargs):
        super(BackButton, self).__init__(**kwargs)

        self.background_color = [1, 1, 1, 1]
        self.size_hint = (None, None)
        self.size = (100, 50)
        self.text = "Back"

        self.screen_instance = screen_instance

    def on_press(self):
        App.get_running_app().root.remove_widget(self.screen_instance)
        App.get_running_app().root.transition.direction = "right"
        App.get_running_app().root.current = "home"


class MidiButton(Button):
    def __init__(self, midi_note, first_note, total_duration, **kwargs):
        super(MidiButton, self).__init__(**kwargs)

        self.background_color = [1, 1, 1, 1]
        self.size_hint = (None, None)

        self.size = (100 * midi_note.played_time, 50)

        self.pos = (50 + (midi_note.start_time/total_duration)*((total_duration + 1)*100), ((first_note - midi_note.note)/Window.height) + Window.height/2)
        self.text = midi_note.name
        self.padding = (10, 10)

        self.start_time = midi_note.start_time
        self.end_time = midi_note.end_time
        self.played_time = midi_note.played_time

    def on_press(self):
        self.background_color = [0, 1, 0, 1]

    def on_release(self):
        self.background_color = [1, 1, 1, 1]


class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

        screen = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)

        songs = [x for x in os.listdir("../data/") if ".txt" in x]

        for song in songs:
            name = song.replace("_", " ").replace(".txt", "")

            layout.add_widget(SongButton(song, text=name))

        screen.add_widget(layout)

        self.add_widget(screen)


class MidiLayout(RelativeLayout):

    def __init__(self, midi_buttons, **kwargs):
        super(MidiLayout, self).__init__(**kwargs)

        self.size_hint = (None, None)

        self.size = ((midi_buttons[-1].end_time + 1) * 100, Window.height)

        for button in midi_buttons:
            self.add_widget(button)

    # def on_touch_down(self, touch):
    #     if touch.is_double_tap:
    #         scroll = ScrollEffect()
    #         scroll.start(-self.window_width)


class MidiSheet(Screen):

    def __init__(self, **kwargs):
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

    def build(self):

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Home(name="home"))

        return sm




