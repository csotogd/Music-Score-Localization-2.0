import numpy as np
from localization.sliding_hashes.create_hashes import create_hashes


class global_hashes:
    song_array = None
    song_idx_dict = None


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


def localize_sample_sh(
    sample_constellation_map: list, song_constellation_map: list, sample_freq=1
):
    """
    A function to perform sample localization. The function first
    creates the hash arrays from the sample and the song constellation
    maps and then finds the indices at which they match. The function then
    looks up the corresponding times in the song index dictionary. The function
    finally returns:
        - A list of the times at which the sample is found to match the song.
            NOTE: Each time in the list is to be interpreted as the STARTING time at
            which the sample matches the song. To get the CURRENT time, the recording time
            needs to be added to the time returned by this function.
        - The matching score for the times in the list.
    """

    if global_hashes.song_array is None:
        song_array, song_idx_dict = create_hashes(song_constellation_map)
        global_hashes.song_array = song_array
        global_hashes.song_idx_dict = song_idx_dict
        print("created new song hashes")

    else:
        song_array = global_hashes.song_array
        song_idx_dict = global_hashes.song_idx_dict

    sample_array, _ = create_hashes(sample_constellation_map)
    matching_indices, matching_score = match(sample_array, song_array)
    matching_times = [song_idx_dict[i] / sample_freq for i in matching_indices]

    # print("match found with seconds: ", matching_times)

    return matching_times, matching_score
