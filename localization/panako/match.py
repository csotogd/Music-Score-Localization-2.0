import numpy as np


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