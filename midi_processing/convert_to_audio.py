"""
This file converts a MIDI file to an audio file. The FluidSynth library is used in order to convert
FluidSynth: https://github.com/FluidSynth/fluidsynth/wiki/UserManual
"""


import os
import re

from midi2audio import FluidSynth
from midi_utils import allowed_formats


def run(file, output_file, sound_font="sound_font.sf2", sample_rate=22050):
    """
    This function converts the MIDI file to an audio file. It first checks if the file exists and is indeed a MIDI
    file. It then checks if the output file is of a valid format. The sound font and sample rate may be overriden.
    Using these parameters, FluidSynth handles the conversion

    Parameters
    ----------
    file : A string of the file to be converted
    output_file : A string of the chosen name and format of the output audio file
    sound_font : A sound font file (.sf2). The sound font of the audio,
                 i.e. how the audio must sound (guitar, piano, etc.)
    sample_rate : An integer indicating the number of samples of audio carried per second, measured in Hz

    Returns
    -------
    void function

    """
    if ".mid" not in file:
        raise Exception(f"{file} is not a MIDI file")

    if not os.path.exists(file):
        raise Exception(f"{file} does not exist")

    if format_allowed(allowed_formats, output_file):
        print(f"Converting {file} to an audio file...")

        fs = FluidSynth(sound_font=sound_font, sample_rate=sample_rate)
        fs.midi_to_audio(file, output_file)

        print(f"Done. Saved as {output_file}")

    else:
        raise Exception(f"{output_file} is not an accepted audio format")


def format_allowed(formats, output_file):
    """
    This function returns a boolean indicating whether the output file is of an allowed format

    Parameters
    ----------
    formats : A list of strings, indicating allowed formats
    output_file : A string indicating the name of the output file

    Returns
    -------
    A boolean True or False
    """

    for f in formats:
        if re.search(f, output_file):
            return True

    return False
