"""
This file gets the notes played from a MIDI file. In order to work, it requires the mido library to get MIDI data:
https://github.com/mido/mido
"""
import sys

import mido as m
import os
from midi_processing.midi_utils import tempo, note_to_name, compute_frequency


class Note:
    """
    A personalised class for a MIDI note that holds the necessary information to create constellation maps
    """

    def __init__(self, note, start_time, end_time, played_time):
        """
        The constructor of the Note class

        Parameters
        ----------
        note : An integer indicating the MIDI note number, usually from 21 to 127
        start_time : A float indicating the time when the note was pressed
        end_time : A float indicating the time when the note was released
        played_time : A float indicating the duration of time for which the note was held
        """
        self.note = note
        self.name = note_to_name(note)
        self.frequency = compute_frequency(note)
        self.start_time = start_time
        self.end_time = end_time
        self.played_time = played_time

    def __str__(self):
        """
        A string representation of the note

        Returns
        -------
        A string indicating the most important information of the MIDI note

        """
        return f"({self.name}:{self.frequency:.2f}): started at {self.start_time:.2f} for {self.played_time:.2f} " \
               f"seconds; ended at {self.end_time:.2f}"

    def __repr__(self):
        """
        Developer-friendly version of the __str__ function

        Returns
        -------
        A string with the features of a MIDI note, indexed by ":"
        """
        return f"{self.note}:{self.name}:{self.frequency:.2f}:{self.start_time:.2f}:{self.end_time:.2f}:{self.played_time:.2f}"


def compute_seconds_elapsed(delta_ticks, ticks_per_beat, midi_tempo):
    """
    A function that computes time in seconds from delta ticks. Delta ticks are the amount of CPU ticks passed since a
    last recorded MIDI message.

    Parameters
    ----------
    delta_ticks : An integer indicating the amount of ticks passed since the last MIDI message
    ticks_per_beat : An integer encoded in a MIDI file. Indicates how many ticks are there in a musical beat
    midi_tempo : An integer for the tempo of the MIDI file/song

    Returns
    -------
    A float indicating the amount of seconds elapsed since the last MIDI message
    """
    return m.tick2second(delta_ticks, ticks_per_beat, midi_tempo)


def get_delta_ticks_since(midi_messages):
    """
    Gets the total amount of ticks since a MIDI message

    Parameters
    ----------
    midi_messages : A list of MIDI messages that occur before the message of interest

    Returns
    -------
    An integer indicating the total amount of ticks passed until a particular message
    """
    total_delta_ticks = 0

    for msg in midi_messages:
        total_delta_ticks += msg.time

    return total_delta_ticks


def get_notes(file):

    """
    Gets all the played notes in a MIDI file. This function iterates through the non-meta MIDI messages and for each
    'note_on', it will find its corresponding 'note_off' and add it to the list of played notes

    In addition, a text file is created with the notes in string format

    Parameters
    ----------
    file : A MIDI file

    Returns
    -------
    A list of Note objects
    """

    if not os.path.exists(file):
        raise Exception(f"{file} does not exist")

    if ".mid" not in file:
        raise Exception(f"{file} is not a MIDI file")

    notes = []

    # clip=True just in case we end up opening a file with notes over 127 velocity (volume),
    # the maximum for a note in a MIDI file
    midi_file = m.MidiFile(file, clip=True)
    ticks_per_beat = midi_file.ticks_per_beat

    for track in midi_file.tracks:

        tempo_msgs = [x for x in track if x.is_meta and x.type == "set_tempo"]

        actual_tempo = tempo if len(tempo_msgs) == 0 else tempo_msgs[0].tempo

        filtered_track = [x for x in track if not x.is_meta and (x.type == "note_on" or x.type == "note_off")]
        i = 0
        for msg in filtered_track:

            note = msg.note

            if msg.type == "note_on":

                # If it's the first note, then there are no other notes preceding it to be taken into account
                if i == 0:
                    start_time = compute_seconds_elapsed(msg.time, ticks_per_beat, actual_tempo)

                else:

                    start_time = compute_seconds_elapsed(msg.time, ticks_per_beat, actual_tempo) + \
                                 compute_seconds_elapsed(get_delta_ticks_since(filtered_track[:i]), ticks_per_beat, actual_tempo)

                # Searches notes ahead, and breaks when it finds the corresponding note_off
                next_messages = filtered_track[i+1:]

                j = 0
                for next_message in next_messages:

                    next_note = next_message.note

                    if next_message.type == "note_off" and next_note == note:

                        end_time = compute_seconds_elapsed(next_message.time, ticks_per_beat, actual_tempo) + \
                                   compute_seconds_elapsed(get_delta_ticks_since(filtered_track[:i+j+1]), ticks_per_beat, actual_tempo)

                        played_time = end_time - start_time

                        notes.append(Note(note, start_time, end_time, played_time))
                        break

                    j += 1
            i += 1

    with open(file.replace(".mid", ".txt"), "w", encoding='utf-8') as f:

        for midi_note in notes:
            f.write(repr(midi_note))
            f.write("\n")

    return notes
