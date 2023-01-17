from localization.direct_comparison.utils import *


class global_hashes:
    song_array = None
    song_idx_dict = None


def localize_sample_d(
    sample_constellation_map: list, song_constellation_map: list, sample_fs=1, song_fs=1
):
    """
    A function to perform sample localization. The function first
    creates the tuple arrays from the sample and the song constellation
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
        song_array, song_idx_dict = create_tuples(song_constellation_map, song_fs)
        global_hashes.song_array = song_array
        global_hashes.song_idx_dict = song_idx_dict
        print("created new song tuples")

    else:
        song_array = global_hashes.song_array
        song_idx_dict = global_hashes.song_idx_dict

    sample_array, _ = create_tuples(sample_constellation_map, sample_fs)
    matching_indices, matching_score = match(sample_array, song_array)
    matching_times = [song_idx_dict[i] for i in matching_indices]

    print("match found with seconds: ", matching_times)

    return matching_times, matching_score
