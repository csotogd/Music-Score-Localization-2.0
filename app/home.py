from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

import os


class Home(App):

    def build(self):

        songs = {}
        for file in os.listdir("/home/diyon335/Desktop/Music Project/Repo/Tests/test_data/"):
            if ".wav" in file:
                songs[file.replace("_", " ").replace(".wav", "")] = file.replace(".wav", ".txt")

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        for song in songs:
            b = Button(text=song, size_hint=(0.5, None), height=40,
                       background_color=(0, 0, 0, 0))

            b.bind(on_press=self.choose_song(songs[song]))
            layout.add_widget(b)

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)

        return root

    def choose_song(self, song_file):
        MidiSheet(song_file).run()


class MidiSheet(App):

    def __init__(self, song_file, **kwargs):
        super().__init__(**kwargs)

        self.song_file = song_file

    def build(self):
        label = Label(text=f"You opened {self.song_file}")

        return label









