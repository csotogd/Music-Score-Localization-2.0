# Append root to path
import sys
import os

sys.path.append(os.getcwd())

# Import methods for testing
from localization.direct_comparison.localize_sample_d import localize_sample_d
from localization.hashing.localize_sample_h import localize_sample_h
from localization.sliding_hashes.localize_sample_sh import localize_sample_sh

METHODS = [localize_sample_d, localize_sample_h, localize_sample_sh]

# Import constellation generators
from random_constellations import random_constellations
from constellations_from_wav_paths import constellations_from_wav_paths

# Time keeping
import time

# Constants for random testing
SONG_LENGTH = 10_000
SAMPLE_LENGTH = 100
NOISE_VAR = 3


def test_loc(method, song_wav_path=None, recording_wav_path=None, random=False):
    if random:
        (
            song_constellation_map,
            sample_constellation_map,
            idx,
            origin,
        ) = random_constellations(
            song_length=SONG_LENGTH, sample_length=SAMPLE_LENGTH, noise_var=NOISE_VAR
        )

    print()
    print("Match testing")
    print()
    print()
    print("Part sampled from constellation map (first 10 tuples):")
    print(song_constellation_map[idx : idx + 10])
    print()
    print("Distorted sample (first 10 tuples):")
    print(sample_constellation_map[:10])
    print()

    start = time.time()
    matching_times, matching_score = method(
        sample_constellation_map, song_constellation_map
    )
    result = "success" if origin in matching_times else "failure"
    end = time.time()
    print(f"Results (method: {method.__name__})")
    print()
    print(f"Sample origin time: {origin}")
    print(f"Matching times: {matching_times} ({result})")
    print(f"Matching score: {matching_score}")
    print(f"Total calculation time: {end-start}")
    print()


if __name__ == "__main__":
    test_loc(method=localize_sample_sh, random=True)
