# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 10
TIME_BITS = 12
TIME_AHEAD = 5


def create_hashes(constellation_map: list):
    hashes = {}
    for i, (t_0, freq_0) in enumerate(constellation_map):
        for t_1, freq_1 in constellation_map[i:]:
            td = t_1 - t_0
            if td > TIME_AHEAD:
                break

            freq_0_bin = int(freq_0 / UPPER_FREQ * (2**FREQ_BITS))
            freq_1_bin = int(freq_1 / UPPER_FREQ * (2**FREQ_BITS))
            td_bin = int(td / TIME_AHEAD * (2**TIME_BITS))

            hash = freq_0_bin | (freq_1_bin << 10) | (td_bin << 20)

            if hash not in hashes:
                hashes[hash] = []
            hashes[hash].append(t_0)

    return hashes


def match(sample_hashes, song_hashes):
    matches = {}
    for hash, _ in sample_hashes.items():
        if hash in song_hashes:
            source_times = song_hashes[hash]
            for source_time in source_times:
                if source_time not in matches:
                    matches[source_time] = 0
                matches[source_time] += 1

    return matches
