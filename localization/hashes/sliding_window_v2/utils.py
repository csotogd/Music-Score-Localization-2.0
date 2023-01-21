from localization.hashes.create_hash import create_hash_shazam, create_hash_panako

IDX_AHEAD = 10


def create_hashes_dict_shazam(constellation_map):
    hashes = {}
    for i, (t_0, freq_0) in enumerate(constellation_map):
        if t_0 not in hashes:
            hashes[t_0] = set()

        for t_1, freq_1 in constellation_map[i + 1 : i + 1 + IDX_AHEAD]:
            hash = create_hash_shazam(t_0, freq_0, t_1, freq_1)
            hashes[t_0].add(hash)

    return hashes


def create_hashes_dict_panako(constellation_map):
    hashes = {}
    for i, (t_0, freq_0) in enumerate(constellation_map):
        if t_0 not in hashes:
            hashes[t_0] = set()

        for j, (t_1, freq_1) in enumerate(constellation_map[i + 1 : i + 1 + IDX_AHEAD]):
            for t_2, freq_2 in constellation_map[j + 1 : j + 1 + IDX_AHEAD]:
                hash = create_hash_panako(t_0, freq_0, t_1, freq_1, t_2, freq_2)
                hashes[t_0].add(hash)

    return hashes


def matches_dict_sw2(sample_hashes: dict, song_hashes: dict):
    sample_hash_sets = list(sample_hashes.values())
    sample_len = len(sample_hash_sets)
    song_hash_sets = list(song_hashes.values())
    song_times = list(song_hashes.keys())
    song_len = len(song_hash_sets)
    matches = {}
    for i in range(song_len - sample_len):
        score = sum(
            len(sample_hash_set.intersection(song_hash_set))
            for sample_hash_set, song_hash_set in zip(
                sample_hash_sets, song_hash_sets[i : i + sample_len]
            )
        )
        matches[song_times[i]] = score

    return matches


def best_matches_sw2(sample_hashes, song_hashes):
    matches = matches_dict_sw2(sample_hashes, song_hashes)
    match_times = []
    max_matches = 0

    for time in matches:
        if matches[time] > max_matches:
            max_matches = matches[time]
            match_times = [time]
        elif matches[time] == max_matches:
            match_times.append(time)

    return match_times, max_matches
