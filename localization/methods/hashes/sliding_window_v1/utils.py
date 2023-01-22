import numpy as np
from localization.methods.hashes.create_hash import (
    create_hash_shazam,
    create_hash_panako,
)

IDX_AHEAD = 10


def create_hashes_array_sw1_shazam(constellation_map):

    index_dict = {}
    hashes_list = []

    arr_ind = 0
    for i, (t_0, freq_0) in enumerate(constellation_map):
        for t_1, freq_1 in constellation_map[i + 1 : i + 1 + IDX_AHEAD]:
            hash = create_hash_shazam(t_0, freq_0, t_1, freq_1)

            hashes_list.append(hash)
            index_dict[arr_ind] = t_0
            arr_ind += 1

    return np.asarray(hashes_list), index_dict


def create_hashes_array_sw1_panako(constellation_map):

    index_dict = {}
    hashes_list = []

    arr_ind = 0

    for i, (t_0, freq_0) in enumerate(constellation_map):
        for j, (t_1, freq_1) in enumerate(constellation_map[i + 1 : i + 1 + IDX_AHEAD]):
            for t_2, freq_2 in constellation_map[j + 1 : j + 1 + IDX_AHEAD]:
                hash = create_hash_panako(t_0, freq_0, t_1, freq_1, t_2, freq_2)

                hashes_list.append(hash)
                index_dict[arr_ind] = t_0
                arr_ind += 1

    return np.asarray(hashes_list).astype(np.uint64), index_dict


def best_matches_sw1(sample_hash_array: np.ndarray, song_hash_array: np.ndarray):
    sample_len = len(sample_hash_array)
    song_len = len(song_hash_array)
    max_score = 0
    indices = []
    for i in range(song_len - sample_len):
        score = np.sum(sample_hash_array == song_hash_array[i : i + sample_len])
        if score > max_score:
            max_score = score
            indices = [i]
        elif score == max_score:
            indices.append(i)

    return indices, max_score / sample_len
