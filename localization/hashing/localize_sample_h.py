from localization.hashing.create_hashes import create_hashes
from localization.hashing.match import match


class global_hashes:
    song_hashes = None


def localize_sample_h(
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

    if global_hashes.song_hashes is None:
        song_hashes = create_hashes(song_constellation_map)
        global_hashes.song_hashes = song_hashes
        print("created new song hashes")

    else:
        song_hashes = global_hashes.song_hashes

    sample_hashes = create_hashes(sample_constellation_map)
    matches = match(sample_hashes, song_hashes)

    match_times = []
    max_matches = 0

    for time in matches:
        if matches[time] > max_matches:
            max_matches = matches[time]
            match_times = [time / sample_freq]
        elif matches[time] == max_matches:
            match_times.append(time / sample_freq)

    return match_times, max_matches


def localize_sample_h_old(matches, sample_freq):

    """
    This function is in charge of localizing the song snippet based on the number of hash matches of
    every time point in the original song

    :param matches: A dictionary where the keys are time points in the original song and values are integer
                    numbers representing the number of hash matches for the time point in the key
    :param sample_freq: A non-integer number representing the sample frequency of the microphone
    :return: A number representing the time point in the original song with the most matches
    """

    """max_matches will keep track of the highest number of matches for some time point found so far"""
    max_matches = 0

    """We iterate over all the time points with matches"""
    for time in matches:

        """If we find a time point with a new maximum match count we update max_matches and store this new
        best matching time in match_time"""
        if matches[time] > max_matches:
            max_matches = matches[time]
            match_time = time

    """match_time is divided by the sample_freq to get an actual time measure in seconds and then returned"""
    return match_time / sample_freq
