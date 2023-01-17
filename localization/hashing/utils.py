# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 10
TIME_AHEAD = 5


def create_hashes(constellation_map: list, fs=1):
    hashes = {}
    for i, (t_0, freq_0) in enumerate(constellation_map):
        t_0 /= fs
        for t_1, freq_1 in constellation_map[i:]:
            t_1 /= fs
            td = t_1 - t_0

            if td > TIME_AHEAD:
                break

            freq_0_binned = freq_0 / UPPER_FREQ * (2**FREQ_BITS)
            freq_1_binned = freq_1 / UPPER_FREQ * (2**FREQ_BITS)

            hash = int(freq_0_binned) | (int(freq_1_binned) << 10) | (int(td) << 20)

            if hash not in hashes:
                hashes[hash] = []
            hashes[hash].append(t_0)

    return hashes


def match(snippet_hashes, song_hashes):
    matches = {}
    for hash, _ in snippet_hashes.items():
        if hash in song_hashes:
            source_times = song_hashes[hash]
            for source_time in source_times:
                if source_time not in matches:
                    matches[source_time] = 0
                matches[source_time] += 1

    return matches
