import numpy as np

# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 10


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
        for t_1, freq_1 in constellation_map[i : i + 10]:
            td = t_1 - t_0

            freq_0_binned = freq_0 / UPPER_FREQ * (2**FREQ_BITS)
            freq_1_binned = freq_1 / UPPER_FREQ * (2**FREQ_BITS)

            hash = (
                int(freq_0_binned)
                | (int(freq_1_binned) << FREQ_BITS)
                | (int(td) << (2 * FREQ_BITS))
            )

            hashes_list.append(hash)
            index_dict[arr_ind] = t_0
            arr_ind += 1

    print(hashes_list)
    return np.asarray(hashes_list), index_dict
