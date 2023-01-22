from localization.methods.hashes.sliding_window_v1.utils_sw1 import *
import time


def localize_sample_sw1(
    sample_constellation_map, song_constellation_map, print_times, hashing_algorithm
):
    start = time.time()

    # Create sample hash array
    if hashing_algorithm == "shazam":
        sample_array, _ = create_hashes_array_sw1_shazam(sample_constellation_map)
    elif hashing_algorithm == "panako":
        sample_array, _ = create_hashes_array_sw1_panako(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample hash array creation time: {sample_check - start}")

    # Create song hash array
    if hashing_algorithm == "shazam":
        song_array, song_idx_dict = create_hashes_array_sw1_shazam(
            song_constellation_map
        )
    elif hashing_algorithm == "panako":
        song_array, song_idx_dict = create_hashes_array_sw1_panako(
            song_constellation_map
        )
    song_check = time.time()
    if print_times:
        print(f"Song hash array creation time: {song_check-sample_check}")

    # Perform localization
    match_indices, match_score = best_matches_sw1(sample_array, song_array)
    match_times = [song_idx_dict[i] for i in match_indices]
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return match_times, match_score


def localize_sample_sw1_shazam(
    sample_constellation_map, song_constellation_map, print_times=False
):
    return localize_sample_sw1(
        sample_constellation_map,
        song_constellation_map,
        print_times,
        hashing_algorithm="shazam",
    )


def localize_sample_sw1_panako(
    sample_constellation_map, song_constellation_map, print_times=False
):
    return localize_sample_sw1(
        sample_constellation_map,
        song_constellation_map,
        print_times,
        hashing_algorithm="panako",
    )
