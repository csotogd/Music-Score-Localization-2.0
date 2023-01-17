from localization.sliding_hashes_new.utils import *


class global_hashes:
    song_hashes = None


def localize_sample_sh_new(
    sample_constellation_map: list, song_constellation_map: list
):

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
