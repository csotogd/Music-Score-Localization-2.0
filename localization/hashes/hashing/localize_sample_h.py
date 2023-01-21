from localization.hashes.hashing.utils import *


def localize_sample_h_shazam(sample_constellation_map, song_constellation_map):
    sample_hashes = create_hashes_dict_shazam(sample_constellation_map)
    song_hashes = create_hashes_dict_shazam(song_constellation_map)
    match_times, max_matches = best_matches_h(sample_hashes, song_hashes)

    return match_times, max_matches


def localize_sample_h_panako(sample_constellation_map, song_constellation_map):
    sample_hashes = create_hashes_dict_panako(sample_constellation_map)
    song_hashes = create_hashes_dict_panako(song_constellation_map)
    match_times, max_matches = best_matches_h(sample_hashes, song_hashes)

    return match_times, max_matches
