from create_hashes import create_hashes
from match import match


def localize_sample(sample_constellation_map: list, song_constellation_map: list):
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

    song_array, song_idx_dict = create_hashes(song_constellation_map)
    sample_array, _ = create_hashes(sample_constellation_map)
    matching_indices, matching_score = match(sample_array, song_array)
    matching_times = [song_idx_dict[i] for i in matching_indices]

    return matching_times, matching_score
