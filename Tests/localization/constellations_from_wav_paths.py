# Append root to path
import sys
import os

sys.path.append(os.getcwd())

# Import signal processing functions
from scipy.io.wavfile import read
from Uttilities.pipelines import sp_pipeline
from Uttilities.Generator_segments import Generator_segments_recorded


def constellations_from_wav_paths(song_path, sample_path):
    song_fs, song = read(song_path)
    song_constellation_map = sp_pipeline(song, song_fs, denoise=False)

    sample_fs, sample = read(sample_path)
    sample_segment_generator = Generator_segments_recorded(
        sample, seconds_per_segment=2, non_overlap_seconds=2
    )

    return song_constellation_map, sample_segment_generator


if __name__ == "__main__":
    song_constellation_map, sample_constellation_map = constellations_from_wav_paths(
        "data/bach_prelude_c_major/Prelude_Bach.wav",
        "data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav",
    )
