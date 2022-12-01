# Append root to path
import sys
import os

sys.path.append(os.getcwd())

# Import signal processing functions
from scipy.io.wavfile import read
from Uttilities.pipelines import sp_pipeline


def constellations_from_wav_paths(song_path, sample_path):
    song_fs, song = read(song_path)
    song_constellation_map = sp_pipeline(song, song_fs, denoise=False)

    sample_fs, sample = read(sample_path)
    sample_constellation_map = sp_pipeline(sample, sample_fs, denoise=True)

    return song_constellation_map, sample_constellation_map


song_constellation_map, sample_constellation_map = constellations_from_wav_paths(
    "data/bach_prelude_c_major/Prelude_Bach.wav",
    "data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav",
)
