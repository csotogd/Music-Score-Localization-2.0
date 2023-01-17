from localization.sliding_hashes_new.utils import *


class global_hashes:
    song_hashes = None


def localize_sample_sh_new(
    sample_constellation_map: list, song_constellation_map: list, sample_freq=1
):

    if global_hashes.song_hashes is None:
        song_hashes = create_hashes(song_constellation_map, sample_freq)
        global_hashes.song_hashes = song_hashes
        print("created new song hashes")
        print()

    else:
        song_hashes = global_hashes.song_hashes

    sample_hashes = create_hashes(sample_constellation_map, sample_freq)
    matches = match(sample_hashes, song_hashes)
    matching_score = max(matches.values())
    matching_times = [
        time / sample_freq for time in matches if matches[time] == matching_score
    ]

    # print("match found with seconds: ", matching_times)

    return matching_times, matching_score
