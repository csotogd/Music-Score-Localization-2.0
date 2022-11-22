from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

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
        self.size_hint = (0.1, 0.1)
        self.text = "Back"

        self.screen_instance = screen_instance

    def on_press(self):
        App.get_running_app().root.remove_widget(self.screen_instance)
        App.get_running_app().root.transition.direction = "right"
        App.get_running_app().root.current = "home"


class MidiButton(Button):
    def __init__(self, name, pos_x, pos_y, **kwargs):
        super(MidiButton, self).__init__(**kwargs)

        self.background_color = [1, 1, 1, 1]
        self.size_hint = (0.1, 0.1)
        self.pos = (pos_x, pos_y)
        self.text = name
        self.padding = (10, 10)

    def on_press(self):
        self.background_color = [0, 1, 0, 1] if self.background_color == [1, 1, 1, 1] else [1, 1, 1, 1]


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


class MidiSheet(Screen):

    def __init__(self, **kwargs):
        super(MidiSheet, self).__init__(**kwargs)

        screen = ScrollView(size=(Window.width, Window.height), do_scroll_x=True, do_scroll_y=False)

        notes = get_notes_in_song("../data/" + self.name)

        layout = RelativeLayout(size=(Window.width, Window.height))
        layout.add_widget(BackButton(self))

        initial_y_pos = Window.height/2
        initial_x_pos = Window.width*0.1
        for note in notes:
            note_name = note.split(":")[1]

            layout.add_widget(MidiButton(note_name, initial_x_pos, initial_y_pos))

            initial_x_pos += 100

        screen.add_widget(layout)

        self.add_widget(screen)


class Localiser(App):

    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Home(name="home"))

        return sm





