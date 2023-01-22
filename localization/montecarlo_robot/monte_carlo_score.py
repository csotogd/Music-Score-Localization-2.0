from localization.methods.hashes.sliding_window_v2.utils_sw2 import *


def monte_carlo_score(
    sample_constellation_map, song_constellation_map, hashing_algorithm
):

    # Create sample hash dictionary
    if hashing_algorithm == "shazam":
        sample_hashes = create_hashes_dict_sw2_shazam(sample_constellation_map)
    elif hashing_algorithm == "panako":
        sample_hashes = create_hashes_dict_sw2_panako(sample_constellation_map)

    # Create song hash dictionary
    if hashing_algorithm == "shazam":
        song_hashes = create_hashes_dict_sw2_shazam(song_constellation_map)
    elif hashing_algorithm == "panako":
        song_hashes = create_hashes_dict_sw2_panako(song_constellation_map)

    mc_score_dict = matches_dict_sw2(sample_hashes, song_hashes)

    return mc_score_dict


def monte_carlo_score_shazam(sample_constellation_map, song_constellation_map):
    return monte_carlo_score(
        sample_constellation_map, song_constellation_map, hashing_algorithm="shazam"
    )


def monte_carlo_score_panako(sample_constellation_map, song_constellation_map):
    return monte_carlo_score(
        sample_constellation_map, song_constellation_map, hashing_algorithm="panako"
    )
