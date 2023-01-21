from localization.hashes.sliding_window_v1.utils import *


def localize_sample_sw1_shazam(sample_constellation_map, song_constellation_map):
    sample_array, _ = create_hashes_array_shazam(sample_constellation_map)
    song_array, song_idx_dict = create_hashes_array_shazam(song_constellation_map)
    match_indices, matching_score = best_matches_sw1(sample_array, song_array)
    match_times = [song_idx_dict[i] for i in match_indices]

    return match_times, matching_score


def localize_sample_sw1_panako(sample_constellation_map, song_constellation_map):
    sample_array, _ = create_hashes_array_panako(sample_constellation_map)
    song_array, song_idx_dict = create_hashes_array_panako(song_constellation_map)
    match_indices, matching_score = best_matches_sw1(sample_array, song_array)
    match_times = [song_idx_dict[i] for i in match_indices]

    return match_times, matching_score
