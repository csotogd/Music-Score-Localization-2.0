from create_hashes import create_hashes
from match import match

song_constellation_map = [
    (0, 20),
    (1, 200),
    (1, 300),
    (2, 40),
    (2, 50),
    (3, 60),
    (3, 100),
    (4, 50),
    (5, 40),
    (6, 40),
    (6, 50),
    (7, 60),
]

sample_constellation_map = [(0, 40), (0, 50), (1, 60), (2, 100)]

time_ahead = 5

song_hashes = create_hashes(song_constellation_map, time_ahead)
print(song_hashes)

print()
sample_hashes = create_hashes(sample_constellation_map, time_ahead)
print(sample_hashes)

print()
matches = match(sample_hashes, song_hashes)

print(matches)
