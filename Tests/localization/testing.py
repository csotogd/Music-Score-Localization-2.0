# Append root to path
import sys
import os

sys.path.append(os.getcwd())

# Import methods for testing
from localization.direct_comparison.localize_sample_d import localize_sample_d
from localization.hashing.localize_sample_h import localize_sample_h
from localization.sliding_hashes.localize_sample_sh import localize_sample_sh
from localization.sliding_hashes_new.localize_sample_sh_new import (
    localize_sample_sh_new,
)
from localization.panako_sh.localize_sample_panako_sh import localize_sample_panako_sh
from localization.panako_h.localize_sample_panako_h import localize_sample_panako_h

METHODS = [
    localize_sample_d,
    localize_sample_h,
    localize_sample_sh,
    localize_sample_sh_new,
    localize_sample_panako_sh,
    localize_sample_panako_h,
]

# Import constellation generator
from random_constellations import random_constellations

# Time keeping
import time

# Constants for random testing
SONG_LENGTH = 10_000  # 132_300  # 220_500, 441_000
SAMPLE_LENGTH = 100  # 2004  # 35, 125, 501, 2004, 3371
NOISE_VAR = 3
ERROR_MARGIN = 2


def random_test(method):
    (
        song_constellation_map,
        sample_constellation_map,
        idx,
        origin,
    ) = random_constellations(
        song_length=SONG_LENGTH,
        sample_length=SAMPLE_LENGTH,
        noise_var=NOISE_VAR,
    )

    print()
    print("Match testing")
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
    result = (
        "Success"
        if any(
            matching_time - ERROR_MARGIN <= origin <= matching_time + ERROR_MARGIN
            for matching_time in matching_times
        )
        else "Failure"
    )
    end = time.time()
    print(f"Results (method: {method.__name__})")
    print()
    print(f"Sample origin time: {origin}")
    print(f"Matching times: {matching_times}")
    print(f"Result: {result}")
    print(f"Matching score: {matching_score}")
    print(f"Total calculation time: {end-start}")
    print()


if __name__ == "__main__":
    random_test(method=localize_sample_sh_new)
