from localization.panako_h.create_hashes import create_hashes


class global_hashes:
    song_hashes = None


def match(sample_hashes, song_hashes):

    """
    This function is in charge of computing matches between hashes of a snippet recorded by
    the microphone and the hashes of the original song

    :param snippet_hashes: A dictionary containing the hashes in the song snippet, keys are hashes and values
                            are lists of points in time associated to the hash in the key
    :param song_hashes: A dictionary contaning the hashes in the original song, same structure as before
    :return: The function returns a dictionary where the keys are time points in the original song and values
            are integer numbers of hashes associated to the time point in the key
    """

    """The "matches" dictioanry that will be returned at the end is initialized"""
    matches = {}

    """We iterate over hashes computed over the song snippet recorded by the microphone;
    _ are the snippet time points, which are not needed"""
    for hash, _ in sample_hashes.items():

        """If the hash currently being evaluated is also found in the hashes of the original song
        it means we have two matching diagonals in the song constellation map and snippet
        constellation map"""
        if hash in song_hashes:

            """Given a hash in the original song with a match we want to retrieve the time points
            in the original song associated to it"""
            source_times = song_hashes[hash]

            for source_time in source_times:

                """For every new time point found with some matching hashes we initialize its
                match count in the "matches" dictionary as 0, then we increase it by 1"""
                if source_time not in matches:
                    matches[source_time] = 0
                matches[source_time] += 1

    return matches


def localize_sample_panako_h(
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
