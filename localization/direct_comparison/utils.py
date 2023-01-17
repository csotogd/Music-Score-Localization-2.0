import numpy as np

TIME_AHEAD = 5

# A constant that defines the thresholds for comparing two tuples of the form
# (freq_0, freq_1, td) to account for frequency and time distortion.
RANGES = np.array((2, 2, 1))


def create_tuples(constellation_map: list):
    """
    A function that creates an array containing the tuples
    representing the diagonals in the constellation map.
    The tuples are in the form (freq_0, freq_1, td) where:
        - freq_0 is a frequency encountered at time t_0;
        - freq_1 is a frequency encountered at time t_1 > t_0;
        - td = t_1 - t_0.

    The function returns:
        - A numpy array containing the tuples as its rows;
        - A dictionary in which each each index in the numpy
        array is associated with the t_0 for the corresponding
        tuple found at that index in the array.
    """

    index_dict = {}
    tuples_list = []

    arr_ind = 0
    for i, (t_0, freq_0) in enumerate(constellation_map):
        for t_1, freq_1 in constellation_map[i:]:
            td = t_1 - t_0
            if td > TIME_AHEAD:
                break
            tuples_list.append((freq_0, freq_1, td))
            index_dict[arr_ind] = t_0
            arr_ind += 1

    return np.asarray(tuples_list), index_dict


def match(sample_tuples_array: np.ndarray, song_tuples_array: np.ndarray):
    """
    A function which compares the sample tuple array with the song
    tuple array by sliding the first over the second and counting
    the total number of matches (within a threshold as defined by the
    RANGES constant). The function returns:
        - the indices at which the maximum number of matches were found;
        - the number of matches divided by the length or the sample tuple array.
    """

    sample_len = len(sample_tuples_array)
    song_len = len(song_tuples_array)
    max_score = 0
    indices = []
    for i in range(song_len - sample_len):
        score = np.sum(
            np.all(
                np.abs(sample_tuples_array - song_tuples_array[i : i + sample_len])
                < RANGES,
                axis=1,
            )
        )
        if score > max_score:
            max_score = score
            indices = [i]
        elif score == max_score:
            indices.append(i)

    return indices, max_score / sample_len
