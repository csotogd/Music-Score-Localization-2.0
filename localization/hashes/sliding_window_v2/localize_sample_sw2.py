from localization.hashes.sliding_window_v2.utils import *


def localize_sample_sw2_shazam(sample_constellation_map, song_constellation_map):
    sample_hashes = create_hashes_dict_shazam(sample_constellation_map)
    song_hashes = create_hashes_dict_shazam(song_constellation_map)
    match_times, match_score = best_matches_sw2(sample_hashes, song_hashes)

    return match_times, match_score


def localize_sample_sw2_panako(sample_constellation_map, song_constellation_map):
    sample_hashes = create_hashes_dict_panako(sample_constellation_map)
    song_hashes = create_hashes_dict_panako(song_constellation_map)
    match_times, match_score = best_matches_sw2(sample_hashes, song_hashes)

    return match_times, match_score
