# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 10
TIME_BITS = 12
TIME_AHEAD = 5


def create_hashes(constellation_map: list):
    hashes = {}
    for i, (t_0, freq_0) in enumerate(constellation_map):
        if t_0 not in hashes:
            hashes[t_0] = set()

        for t_1, freq_1 in constellation_map[i:]:
            td = t_1 - t_0

            if td > TIME_AHEAD:
                break

            freq_0_bin = int(freq_0 / UPPER_FREQ * (2**FREQ_BITS))
            freq_1_bin = int(freq_1 / UPPER_FREQ * (2**FREQ_BITS))
            td_bin = int(td / TIME_AHEAD * (2**TIME_BITS))

            hash = freq_0_bin | (freq_1_bin << 10) | (td_bin << 20)

            hashes[t_0].add(hash)

    return hashes


def match(sample_hashes: dict, song_hashes: dict):
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
