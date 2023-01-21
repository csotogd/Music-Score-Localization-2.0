from localization.diagonals.utils import *


def localize_sample_d(sample_constellation_map: list, song_constellation_map: list):
    song_array, song_idx_dict = create_tuples_array(song_constellation_map)
    sample_array, _ = create_tuples_array(sample_constellation_map)
    matching_indices, matching_score = best_matches_d(sample_array, song_array)
    matching_times = [song_idx_dict[i] for i in matching_indices]

    return matching_times, matching_score
