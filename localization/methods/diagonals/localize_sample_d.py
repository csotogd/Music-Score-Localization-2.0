from localization.methods.diagonals.utils import *
import time


def localize_sample_d(
    sample_constellation_map, song_constellation_map, print_times=False
):
    start = time.time()
    sample_array, _ = create_tuples_array(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample diag array creation time: {sample_check-start}")
    song_array, song_idx_dict = create_tuples_array(song_constellation_map)
    song_check = time.time()
    if print_times:
        print(f"Song diag array creation time: {song_check-sample_check}")
    matching_indices, matching_score = best_matches_d(sample_array, song_array)
    matching_times = [song_idx_dict[i] for i in matching_indices]
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return matching_times, matching_score
