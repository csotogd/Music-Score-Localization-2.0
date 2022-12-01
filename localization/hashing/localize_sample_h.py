def localize_sample_h(matches, sample_freq):

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
