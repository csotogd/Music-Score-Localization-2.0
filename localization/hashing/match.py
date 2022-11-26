def match(snippet_hashes, song_hashes):

    '''
    This function is in charge of computing matches between hashes of a snippet recorded by
    the microphone and the hashes of the original song

    :param snippet_hashes: A dictionary containing the hashes in the song snippet, keys are hashes and values
                            are lists of points in time associated to the hash in the key
    :param song_hashes: A dictionary contaning the hashes in the original song, same structure as before
    :return: The function returns a dictionary where the keys are time points in the original song and values
            are integer numbers of hashes associated to the time point in the key
    '''

    '''The "matches" dictioanry that will be returned at the end is initialized'''
    matches = {}

    '''We iterate over hashes computed over the song snippet recorded by the microphone;
    _ are the snippet time points, which are not needed'''
    for hash, _ in snippet_hashes.items():

        '''If the hash currently being evaluated is also found in the hashes of the original song
        it means we have two matching diagonals in the song constellation map and snippet
        constellation map'''
        if hash in song_hashes:

            '''Given a hash in the original song with a match we want to retrieve the time points
            in the original song associated to it'''
            source_times = song_hashes[hash]

            for source_time in source_times:

                '''For every new time point found with some matching hashes we initialize its
                match count in the "matches" dictionary as 0, then we increase it by 1'''
                if source_time not in matches:
                    matches[source_time] = 0
                matches[source_time] += 1

    return matches
