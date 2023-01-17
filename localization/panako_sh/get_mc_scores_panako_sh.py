import numpy as np
from localization.panako_sh.create_hashes import create_hashes


class global_hashes:
    song_array = None
    song_idx_dict = None


def match(sample_hash_array: np.ndarray, song_hash_array: np.ndarray):
    sample_len = len(sample_hash_array)
    song_len = len(song_hash_array)
    scores = []
    for i in range(song_len - sample_len):
        score = np.sum(sample_hash_array == song_hash_array[i : i + sample_len])
        scores.append(score)

    return scores


def get_mc_scores_panako_sh(
    sample_constellation_map: list, song_constellation_map: list, sample_freq=1
):

    if global_hashes.song_array is None:
        song_array, song_idx_dict = create_hashes(song_constellation_map)
        global_hashes.song_array = song_array
        global_hashes.song_idx_dict = song_idx_dict
        print("created new song hashes")

    else:
        song_array = global_hashes.song_array
        song_idx_dict = global_hashes.song_idx_dict

    sample_array, _ = create_hashes(sample_constellation_map)
    scores = match(sample_array, song_array)
    mc_scores = {song_idx_dict[i] / sample_freq: scores[i] for i in scores}

    # print("match found with seconds: ", matching_times)

    return mc_scores
