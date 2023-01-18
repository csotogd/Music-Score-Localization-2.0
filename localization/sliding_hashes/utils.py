import numpy as np

# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 10
TIME_BITS = 12
TIME_AHEAD = 2


def create_hashes(constellation_map: list):
    """
    A function that creates an array containing the hashes
    representing the diagonals in the constellation map.
    The two frequencies are normalised to the range [0, 1023]
    and then stored as 10-bit integers, while the time difference
    is stored as a 12-bit integer, thus creating a 32-bit integer
    hash.

    The function returns:
        - A numpy array (vector) containing the hashes;
        - A dictionary in which each each index in the numpy
        array is associated with the time in the song at which
        the corresponding hash is encountered.
    """

    index_dict = {}
    hashes_list = []

    arr_ind = 0
    for i, (t_0, freq_0) in enumerate(constellation_map):
        for t_1, freq_1 in constellation_map[i:]:
            td = t_1 - t_0

            if td > TIME_AHEAD:
                break

            freq_0_bin = int((freq_0 / UPPER_FREQ) * (2**FREQ_BITS))
            freq_1_bin = int((freq_1 / UPPER_FREQ) * (2**FREQ_BITS))
            # td_bin = int((td / TIME_AHEAD) * (2**TIME_BITS))

            hash = freq_0_bin | (freq_1_bin << 10) | (int(td) << 20)

            hashes_list.append(hash)
            index_dict[arr_ind] = t_0
            arr_ind += 1

    return np.asarray(hashes_list), index_dict


def match(sample_hash_array: np.ndarray, song_hash_array: np.ndarray):
    """
    A function which compares the sample hash array with the song
    hash array by sliding the first over the second and counting
    the total number of matches. The function returns:
        - the indices at which the maximum number of matches were found;
        - the number of matches divided by the length or the sample tuple array.
    """

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
