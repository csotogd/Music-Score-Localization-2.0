
"""
The allowed formats can be modified here. According to FluidSynth, .flac is recommended
"""
allowed_formats = [".mp3", ".wav", ".flac"]

"""
The beats per minute of the song
"""
bpm = 79

"""
Computes the tempo of the MIDI file depending on the bpm
"""
tempo = 60000000/bpm

"""
A list of musical notes
"""
notes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]


def note_to_name(midi_note):
    """
    A function that converts a MIDI note number to a musical note in string format

    Parameters
    ----------
    midi_note : An integer indicating the MIDI note

    Returns
    -------
    A string indicating the musical note
    """
    return notes[midi_note % 12] + str(int(midi_note/12 - 1))


def compute_frequency(midi_note):
    """
    A function that computes the frequency of a musical note from its respective MIDI note

    Parameters
    ----------
    midi_note : An integer indicating the MIDI note

    Returns
    -------
    A float indicating the frequency (in Hz) of the MIDI note
    """
    return 440 * 2 ** ((midi_note - 69) / 12)
