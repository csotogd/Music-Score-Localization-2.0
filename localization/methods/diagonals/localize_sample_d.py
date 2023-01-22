from localization.methods.diagonals.utils import *
import time


def localize_sample_d(
    sample_constellation_map, song_constellation_map, print_times=False
):
    start = time.time()

    # Create sample diagonal array
    sample_array, _ = create_diag_array(sample_constellation_map)
    sample_check = time.time()
    if print_times:
        print(f"Sample diagonal array creation time: {sample_check-start}")

    # Create song diagonal array
    song_array, song_idx_dict = create_diag_array(song_constellation_map)
    song_check = time.time()
    if print_times:
        print(f"Song diagonal array creation time: {song_check-sample_check}")

    # Perform localization
    match_indices, match_score = best_matches_d(sample_array, song_array)
    match_times = [song_idx_dict[i] for i in match_indices]
    localization_check = time.time()
    if print_times:
        print(f"Localization time: {localization_check-song_check}")
        print()

    return match_times, match_score
