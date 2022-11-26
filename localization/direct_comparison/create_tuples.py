import numpy as np


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
        for t_1, freq_1 in constellation_map[i : i + 10]:

            td = t_1 - t_0

            if td < 1 or td > 10:
                continue

            tuples_list.append((freq_0, freq_1, td))
            index_dict[arr_ind] = t_0
            arr_ind += 1

    return np.asarray(tuples_list), index_dict
