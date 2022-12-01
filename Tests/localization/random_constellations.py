import random


def random_constellations(song_length, sample_length, noise_var):
    song_constellation_map_1 = [
        (time, random.randint(20, 20_000)) for time in range(song_length)
    ]
    song_constellation_map_2 = [
        (time, random.randint(20, 20_000)) for time in range(song_length)
    ]
    song_constellation_map = song_constellation_map_1 + song_constellation_map_2
    song_constellation_map.sort()

    idx = random.randint(0, song_length - sample_length)
    extracted_sample = song_constellation_map[idx : idx + sample_length]

    sample_constellation_map = []
    origin = extracted_sample[0][0]
    for t, freq in extracted_sample:
        sample_constellation_map.append(
            (t - origin, round(freq + random.gauss(0, noise_var)))
        )

    return song_constellation_map, sample_constellation_map, idx, origin
