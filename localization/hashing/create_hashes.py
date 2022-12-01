def create_hashes(constellation_map, time_ahead):

    """
    This function is in charge of constructing a dictionary of lists holding information about
    the diagonals of the music piece. This function is called for both the original song and for
    the snippets recorded by the microphone.

    :param constellation_map: a list of tuples; the tuples are made up of two elements, the first element
                            is a point in time and the second element is the frequency for a peak at that time
    :param time_ahead: a integer used to determine how far ahead in time points in the constellation map
                        should be used to build diagonals
    :return: Returns a dictionary holding all the hashes as keys and the values are lists containing the
            points in time associated to such a hash
    """

    """The "hashes" dictionary that will be returned at the end is initialized"""
    hashes = {}
    upper_frequency = 23_000
    frequency_bits = 10

    """We iterate over all the tuples in the constellation map, retrieving also the index of the
    tuple we are currently looking at"""
    for idx, (time, freq) in enumerate(constellation_map):

        """Next we iterate over all the following tuples in the same constellation map to compute diagonals"""
        for future_time, future_freq in constellation_map[idx:]:

            """We only want to copmute diagonals up to a certain time point in the future, so once we reach a
            tuple for peak that is too far in time we break"""
            if future_time > time + time_ahead:
                break

            """Time difference between the two points in time is computed and frequencies are binned
            for the purposes of hash calculation"""
            time_diff = future_time - time
            freq_binned = freq / upper_frequency * (2**frequency_bits)
            future_freq_binned = future_freq / upper_frequency * (2**frequency_bits)

            hash = (
                int(freq_binned)
                | (int(future_freq_binned) << 10)
                | (int(time_diff) << 20)
            )

            """For every new hash found a new empty list is initialized and added to the dictionary,
            then the time associated to the currently computed diagonal is appended to it"""
            if hash not in hashes:
                hashes[hash] = []
            hashes[hash].append(time)

    return hashes
