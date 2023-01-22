from localization.methods.hashes.sliding_window_v1.utils import *
import time


def localize_sample_sw1_shazam(
    sample_constellation_map, song_constellation_map, print_times=False
):
    start = time.time()
    sample_array, _ = create_hashes_array_shazam(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample hash array creation time: {sample_check - start}")
    song_array, song_idx_dict = create_hashes_array_shazam(song_constellation_map)
    song_check = time.time()
    if print_times:
        print(f"Song hash array creation time: {song_check-sample_check}")
    match_indices, matching_score = best_matches_sw1(sample_array, song_array)
    match_times = [song_idx_dict[i] for i in match_indices]
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return match_times, matching_score


def localize_sample_sw1_panako(
    sample_constellation_map, song_constellation_map, print_times=False
):
    start = time.time()
    sample_array, _ = create_hashes_array_panako(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample hash array creation time: {sample_check - start}")
    song_array, song_idx_dict = create_hashes_array_panako(song_constellation_map)
    song_check = time.time()
    if print_times:
        print(f"Song hash array creation time: {song_check-sample_check}")
    match_indices, matching_score = best_matches_sw1(sample_array, song_array)
    match_times = [song_idx_dict[i] for i in match_indices]
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return match_times, matching_score
