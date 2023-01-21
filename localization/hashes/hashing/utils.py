from localization.hashes.create_hash import create_hash_shazam, create_hash_panako


IDX_AHEAD = 10


def create_hashes_dict_shazam(constellation_map):
    hashes = {}
    for i, (t_0, freq_0) in enumerate(constellation_map):
        for t_1, freq_1 in constellation_map[i + 1 : i + 1 + IDX_AHEAD]:
            hash = create_hash_shazam(t_0, freq_0, t_1, freq_1)

            if hash not in hashes:
                hashes[hash] = []
            hashes[hash].append(t_0)

    return hashes


def create_hashes_dict_panako(constellation_map):
    hashes = {}

    for i, (t_0, freq_0) in enumerate(constellation_map):
        for j, (t_1, freq_1) in enumerate(constellation_map[i + 1 : i + IDX_AHEAD + 1]):
            for t_2, freq_2 in constellation_map[j + 1 : j + IDX_AHEAD + 1]:

                hash = create_hash_panako(t_0, freq_0, t_1, freq_1, t_2, freq_2)

                if hash not in hashes:
                    hashes[hash] = []
                hashes[hash].append(t_0)

    return hashes


def matches_dict_h(sample_hashes, song_hashes):
    matches = {}
    for hash, _ in sample_hashes.items():
        if hash in song_hashes:
            source_times = song_hashes[hash]
            for source_time in source_times:
                if source_time not in matches:
                    matches[source_time] = 0
                matches[source_time] += 1

    return matches


def best_matches_h(sample_hashes, song_hashes):
    matches = matches_dict_h(sample_hashes, song_hashes)
    match_times = []
    max_matches = 0

    for time in matches:
        if matches[time] > max_matches:
            max_matches = matches[time]
            match_times = [time]
        elif matches[time] == max_matches:
            match_times.append(time)

    return match_times, max_matches
