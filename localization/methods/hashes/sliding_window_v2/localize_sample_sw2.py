from localization.methods.hashes.sliding_window_v2.utils import *
import time


def localize_sample_sw2_shazam(
    sample_constellation_map, song_constellation_map, print_times=False
):
    start = time.time()
    sample_hashes = create_hashes_dict_shazam(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample hash dict creation time: {sample_check-start}")
    song_hashes = create_hashes_dict_shazam(song_constellation_map)
    song_check = time.time()
    if print_times:
        print(f"Song hash dict creation time: {song_check-sample_check}")
    match_times, match_score = best_matches_sw2(sample_hashes, song_hashes)
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return match_times, match_score


def localize_sample_sw2_panako(
    sample_constellation_map, song_constellation_map, print_times=False
):
    start = time.time()
    sample_hashes = create_hashes_dict_panako(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample hash dict creation time: {sample_check-start}")
    song_hashes = create_hashes_dict_panako(song_constellation_map)
    song_check = time.time()
    if print_times:
        print(f"Song hash dict creation time: {song_check-sample_check}")
    match_times, match_score = best_matches_sw2(sample_hashes, song_hashes)
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return match_times, match_score
