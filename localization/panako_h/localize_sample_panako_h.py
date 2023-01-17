from localization.panako_h.utils import *


class global_hashes:
    song_hashes = None


def localize_sample_panako_h(
    sample_constellation_map: list, song_constellation_map: list
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

    if global_hashes.song_hashes is None:
        song_hashes = create_hashes(song_constellation_map)
        global_hashes.song_hashes = song_hashes
        print("created new song hashes")
        print()

    else:
        song_hashes = global_hashes.song_hashes

    sample_hashes = create_hashes(sample_constellation_map)
    matches = match(sample_hashes, song_hashes)

    match_times = []
    max_matches = 0

    for time in matches:
        if matches[time] > max_matches:
            max_matches = matches[time]
            match_times = [time]
        elif matches[time] == max_matches:
            match_times.append(time)

    return match_times, max_matches
