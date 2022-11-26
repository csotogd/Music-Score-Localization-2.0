from localization.create_hashes import create_hashes
from localization.match import match
from localization.localize_snippet import localize_snippet
import time


class global_hashes:
    song_hashes = None

def localization_pipeline(song_constellation_map, snippet_constellation_map, time_ahead, sample_freq):

    '''
    :param song_constellation_map: a list of tuples representing the peaks expected based on the original
                                    musci sheet
    :param snippet_constellation_map: a list of tuples represented the peaks recorded by the microphone
                                    in a certain amount of time
    :param time_ahead: a integer used to determine how far ahead in time points in the constellation map
                        should be used to build diagonals
    :param sample_freq: A non-integer number representing the sample frequency of the microphone
    :return: None
    '''

    if global_hashes.song_hashes is None:

        song_hashes = create_hashes(song_constellation_map, time_ahead)
        global_hashes.song_hashes= song_hashes

    else:
        song_hashes = global_hashes.song_hashes

    snippet_hashes = create_hashes(snippet_constellation_map, time_ahead)

    matches = match(snippet_hashes, song_hashes)

    match_time = localize_snippet(matches, sample_freq)

    return match_time

if __name__ == "__main__":
    localization_pipeline()